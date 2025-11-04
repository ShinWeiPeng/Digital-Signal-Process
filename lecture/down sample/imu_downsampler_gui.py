#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMU Raw Data Downsampler (Tkinter GUI) — Responsive Reflow + Min Size

- 多檔選取、預設 Decimate、滑鼠懸浮提示（同上一版）
- 新增：視窗縮小時自動「重排版」（wide <-> narrow）
- 新增：設定最小視窗尺寸，避免擠到看不見
"""
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
from tkinter import Tk, StringVar, DoubleVar, IntVar, ttk, filedialog, messagebox, Toplevel, Label

# ---------- Parsing utilities ----------

NUM_RE = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$')
FS_LINE_RE_INLINE = re.compile(r'^(取樣頻率)\s*[:：]\s*([0-9.]+)\s*$')
ACC_COUNT_RE = re.compile(r'^([XYZ])\s*Acc\s*Data\s*:\s*(\d+)\s*$', re.IGNORECASE)

@dataclass
class IMUFile:
    raw_lines: List[str]
    fs: float
    axis_data: Dict[str, List[float]]  # 'X','Y','Z' -> samples
    count_positions: List[Tuple[int, str, int]]  # (line_index, axis, original_count)

def read_text_lines(path: str) -> List[str]:
    for enc in ('utf-8-sig', 'utf-8', 'cp950', 'big5'):
        try:
            with open(path, 'r', encoding=enc, newline='') as f:
                return f.read().splitlines(True)
        except Exception:
            continue
    with open(path, 'rb') as f:
        return f.read().decode('utf-8', errors='replace').splitlines(True)

def parse_sampling_rate(lines: List[str]) -> Tuple[float, List[str]]:
    for i, ln in enumerate(lines):
        if ln.strip() == '取樣頻率' and i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            try:
                fs = float(nxt)
                return fs, lines
            except ValueError:
                pass
    for i, ln in enumerate(lines):
        m = FS_LINE_RE_INLINE.match(ln.strip())
        if m:
            fs = float(m.group(2))
            return fs, lines
    return 1000.0, lines

def parse_axes(lines: List[str]) -> Tuple[Dict[str, List[float]], List[Tuple[int, str, int]]]:
    axis_data: Dict[str, List[float]] = {}
    positions: List[Tuple[int, str, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        m = ACC_COUNT_RE.match(lines[i].strip())
        if m:
            axis = m.group(1).upper()
            count = int(m.group(2))
            start = i + 1
            vals: List[float] = []
            j = start
            while j < n and len(vals) < count:
                s = lines[j].strip()
                if s and NUM_RE.match(s):
                    try:
                        vals.append(float(s))
                    except ValueError:
                        break
                j += 1
            axis_data[axis] = vals
            positions.append((i, axis, count))
            i = j
        else:
            i += 1
    return axis_data, positions

def load_imu_file(path: str) -> IMUFile:
    lines = read_text_lines(path)
    fs, _ = parse_sampling_rate(lines)
    axis_data, positions = parse_axes(lines)
    return IMUFile(raw_lines=lines, fs=fs, axis_data=axis_data, count_positions=positions)

# ---------- Downsample methods ----------

def decimate_every_n(data: List[float], factor: int) -> List[float]:
    return data[::factor] if factor > 0 else data

def block_mean(data: List[float], factor: int) -> List[float]:
    if factor <= 0:
        return data
    out = []
    full = (len(data) // factor) * factor
    for i in range(0, full, factor):
        blk = data[i:i+factor]
        out.append(sum(blk) / factor)
    return out

def linear_resample(data: List[float], fs_in: float, fs_out: float) -> List[float]:
    if fs_out <= 0 or fs_in <= 0 or not data:
        return data
    import math
    ratio = fs_out / fs_in
    new_len = max(1, int(round(len(data) * ratio)))
    if new_len == 1:
        return [data[0]]
    out = [0.0] * new_len
    step = (len(data) - 1) / (new_len - 1)
    for k in range(new_len):
        src = k * step
        i0 = int(math.floor(src))
        i1 = min(i0 + 1, len(data) - 1)
        frac = src - i0
        out[k] = (1.0 - frac) * data[i0] + frac * data[i1]
    return out

# ---------- Writer ----------

def update_sampling_rate_lines(lines: List[str], fs_new: float) -> List[str]:
    out = list(lines)
    for i, ln in enumerate(out):
        if ln.strip() == '取樣頻率' and i + 1 < len(out):
            out[i + 1] = f"{fs_new:.3f}\n"
            return out
    for i, ln in enumerate(out):
        m = FS_LINE_RE_INLINE.match(ln.strip())
        if m:
            out[i] = f"{m.group(1)}:{fs_new:.3f}\n"
            return out
    return out

def write_downsampled(imu: IMUFile, fs_out: float, method: str) -> List[str]:
    fs_in = imu.fs
    lines = list(imu.raw_lines)
    new_axes: Dict[str, List[float]] = {}
    eff_fs_out = fs_out

    if method in ('decimate', 'mean'):
        if fs_out >= fs_in:
            raise ValueError("目標取樣頻率必須小於原始取樣頻率（這是降取樣）。")
        factor = max(1, int(round(fs_in / fs_out)))
        eff_fs_out = fs_in / factor
        for ax, data in imu.axis_data.items():
            if method == 'decimate':
                new_axes[ax] = decimate_every_n(data, factor)
            else:
                new_axes[ax] = block_mean(data, factor)
    elif method == 'linear':
        for ax, data in imu.axis_data.items():
            new_axes[ax] = linear_resample(data, fs_in, fs_out)
    else:
        raise ValueError("未知方法")

    updated = update_sampling_rate_lines(lines, eff_fs_out if method != 'linear' else fs_out)

    out_lines: List[str] = []
    i = 0
    n = len(updated)
    while i < n:
        m = ACC_COUNT_RE.match(updated[i].strip())
        if m:
            ax = m.group(1).upper()
            old_count = int(m.group(2))
            series = new_axes.get(ax, [])
            out_lines.append(f"{ax} Acc Data:{len(series)}\n")
            for v in series:
                out_lines.append(f"{v:.6f}\n")
            i += 1
            skipped = 0
            while i < n and skipped < old_count:
                s = updated[i].strip()
                if s and NUM_RE.match(s):
                    skipped += 1
                i += 1
            continue
        else:
            out_lines.append(updated[i])
            i += 1
    return out_lines

# ---------- Tooltip ----------

class ToolTip:
    def __init__(self, widget, text: str, wrap=420, delay_ms=350):
        self.widget = widget
        self.text = text
        self.wrap = wrap
        self.delay_ms = delay_ms
        self.tip = None
        self._id = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _schedule(self, event=None):
        self._unschedule()
        self._id = self.widget.after(self.delay_ms, self._show)

    def _unschedule(self):
        if self._id:
            try:
                self.widget.after_cancel(self._id)
            except Exception:
                pass
            self._id = None

    def _show(self, event=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tip = Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.attributes("-topmost", True)
        lbl = Label(self.tip, text=self.text, justify='left', relief='solid', borderwidth=1, bg='#ffffe0', wraplength=self.wrap)
        lbl.pack(ipadx=6, ipady=4)
        self.tip.wm_geometry(f"+{x}+{y}")

    def _hide(self, event=None):
        self._unschedule()
        if self.tip is not None:
            try:
                self.tip.destroy()
            except Exception:
                pass
            self.tip = None

# ---------- Tk GUI ----------

DECIMATE_TIP = (
    "取每 N 點 (Decimate)\n"
    "優點：保留原始時序與尖峰、成本最低。\n"
    "缺點：需先低通避免混疊、僅整數倍率。\n"
    "適合：整數分頻、已做低通、要保留衝擊峰值。"
)

MEAN_TIP = (
    "每 N 點平均 (Block Mean)\n"
    "優點：抗雜訊、趨勢穩、具抗混疊效果。\n"
    "缺點：會鈍化尖峰、僅整數倍率、尾端不足丟棄。\n"
    "適合：長時間趨勢/能量指標、降檔案量。"
)

LINEAR_TIP = (
    "線性重取樣 (Linear)\n"
    "優點：支援非整數倍率、易同步、波形平滑。\n"
    "缺點：會平滑尖峰、高頻多時仍可能失真。\n"
    "適合：與他系統頻率對齊、繪圖/後處理。"
)

class App:
    NARROW_THRESHOLD = 640  # px

    def __init__(self, root: Tk):
        self.root = root
        root.title("IMU Downsampler")
        root.geometry("760x280")
        # 設定最小尺寸，避免過度縮小導致元件被擠壓隱形
        root.minsize(600, 280)

        # multiple input paths
        self.in_paths: List[str] = []
        self.in_path_disp = StringVar(value="")
        self.out_dir = StringVar(value="")
        self.fs_in_disp = StringVar(value="-")

        self.fs_out = DoubleVar(value=1000.0)
        # Default to Decimate (0)
        self.method = IntVar(value=0)

        # Main frame
        self.frm = ttk.Frame(root, padding=12)
        self.frm.pack(fill='both', expand=True)

        # Widgets
        self.lbl_in = ttk.Label(self.frm, text="輸入檔案（可多選）：")
        self.ent_in = ttk.Entry(self.frm, textvariable=self.in_path_disp)
        self.btn_in = ttk.Button(self.frm, text="選擇檔案", command=self.pick_inputs)

        self.lbl_out = ttk.Label(self.frm, text="輸出資料夾：")
        self.ent_out = ttk.Entry(self.frm, textvariable=self.out_dir)
        self.btn_out = ttk.Button(self.frm, text="選擇資料夾", command=self.pick_outdir)

        self.lbl_fs_in = ttk.Label(self.frm, text="原始取樣頻率 (顯示第一個檔)：")
        self.val_fs_in = ttk.Label(self.frm, textvariable=self.fs_in_disp)

        self.lbl_fs_out = ttk.Label(self.frm, text="目標取樣頻率 (Hz)：")
        self.ent_fs_out = ttk.Entry(self.frm, textvariable=self.fs_out, width=12)

        self.lbl_method = ttk.Label(self.frm, text="降取樣方法：")
        self.mfrm = ttk.Frame(self.frm)

        self.rb_dec = ttk.Radiobutton(self.mfrm, text="取每 N 點 (Decimate)", variable=self.method, value=0)
        self.rb_mean = ttk.Radiobutton(self.mfrm, text="每 N 點平均 (Block Mean)", variable=self.method, value=1)
        self.rb_lin = ttk.Radiobutton(self.mfrm, text="線性重取樣 (Linear, 可非整數倍率)", variable=self.method, value=2)

        # Tooltips
        ToolTip(self.rb_dec, DECIMATE_TIP)
        ToolTip(self.rb_mean, MEAN_TIP)
        ToolTip(self.rb_lin, LINEAR_TIP)

        self.btn_run = ttk.Button(self.frm, text="開始執行", command=self.run)

        # Initial layout
        self._mode = None
        self._layout_wide()  # default
        self._set_column_weights_wide()

        # Bind resize to auto-switch layout
        self._resize_after = None
        self.root.bind("<Configure>", self._on_resize)

    # ---------- Responsive layout ----------

    def _on_resize(self, event):
        if event.widget is not self.root:
            return
        # debounce
        if self._resize_after:
            try:
                self.root.after_cancel(self._resize_after)
            except Exception:
                pass
        self._resize_after = self.root.after(80, self._apply_resize)

    def _apply_resize(self):
        w = self.root.winfo_width()
        # dynamically wrap radio text
        self._set_wraplength(w)
        if w < self.NARROW_THRESHOLD and self._mode != 'narrow':
            self._layout_narrow()
            self._set_column_weights_narrow()
            self.root.minsize(300, 450)
        elif w >= self.NARROW_THRESHOLD and self._mode != 'wide':
            self._layout_wide()
            self._set_column_weights_wide()
            self.root.minsize(600, 280)

    def _set_wraplength(self, w):
        # radio texts wrap to avoid overflow
        if self._mode == 'narrow':
            wl = max(220, w - 80)
        else:
            wl = max(320, w - 360)
        try:
            self.rb_dec.configure(wraplength=wl)
            self.rb_mean.configure(wraplength=wl)
            self.rb_lin.configure(wraplength=wl)
        except Exception:
            pass

    def _clear_grid(self):
        for child in (self.lbl_in, self.ent_in, self.btn_in,
                      self.lbl_out, self.ent_out, self.btn_out,
                      self.lbl_fs_in, self.val_fs_in,
                      self.lbl_fs_out, self.ent_fs_out,
                      self.lbl_method, self.mfrm,
                      self.rb_dec, self.rb_mean, self.rb_lin,
                      self.btn_run):
            try:
                child.grid_forget()
            except Exception:
                pass
        # re-pack radios into mfrm
        for w in self.mfrm.winfo_children():
            try:
                w.pack_forget()
            except Exception:
                pass
        self.rb_dec.pack(anchor='w')
        self.rb_mean.pack(anchor='w')
        self.rb_lin.pack(anchor='w')

    def _layout_wide(self):
        self._clear_grid()
        self._mode = 'wide'

        # row 0: input
        self.lbl_in.grid(row=0, column=0, sticky='e', pady=4, padx=(0,6))
        self.ent_in.grid(row=0, column=1, sticky='we', pady=4)
        self.btn_in.grid(row=0, column=2, sticky='w', padx=(6,0))

        # row 1: output dir
        self.lbl_out.grid(row=1, column=0, sticky='e', pady=4, padx=(0,6))
        self.ent_out.grid(row=1, column=1, sticky='we', pady=4)
        self.btn_out.grid(row=1, column=2, sticky='w', padx=(6,0))

        # row 2: fs in
        self.lbl_fs_in.grid(row=2, column=0, sticky='e', pady=4, padx=(0,6))
        self.val_fs_in.grid(row=2, column=1, sticky='w', pady=4)

        # row 3: fs out
        self.lbl_fs_out.grid(row=3, column=0, sticky='e', pady=4, padx=(0,6))
        self.ent_fs_out.grid(row=3, column=1, sticky='w', pady=4)

        # row 4: method
        self.lbl_method.grid(row=4, column=0, sticky='ne', pady=(8,4), padx=(0,6))
        self.mfrm.grid(row=4, column=1, sticky='w', pady=(8,4), columnspan=2)

        # row 5: run
        self.btn_run.grid(row=5, column=2, sticky='e', pady=14)

    def _layout_narrow(self):
        self._clear_grid()
        self._mode = 'narrow'

        # input
        self.lbl_in.grid(row=0, column=0, sticky='w', pady=(2,2))
        self.ent_in.grid(row=1, column=0, sticky='we', pady=(0,4))
        self.btn_in.grid(row=2, column=0, sticky='w', pady=(0,8))

        # output
        self.lbl_out.grid(row=3, column=0, sticky='w', pady=(2,2))
        self.ent_out.grid(row=4, column=0, sticky='we', pady=(0,4))
        self.btn_out.grid(row=5, column=0, sticky='w', pady=(0,8))

        # fs in/out
        self.lbl_fs_in.grid(row=6, column=0, sticky='w', pady=(2,2))
        self.val_fs_in.grid(row=7, column=0, sticky='w', pady=(0,8))

        self.lbl_fs_out.grid(row=8, column=0, sticky='w', pady=(2,2))
        self.ent_fs_out.grid(row=9, column=0, sticky='we', pady=(0,8))

        # method
        self.lbl_method.grid(row=10, column=0, sticky='w', pady=(4,2))
        self.mfrm.grid(row=11, column=0, sticky='we', pady=(0,8))

        # run
        self.btn_run.grid(row=12, column=0, sticky='e', pady=(6,4))

    def _set_column_weights_wide(self):
        # 3 columns: [label][entry expansive][button]
        for c in range(3):
            self.frm.columnconfigure(c, weight=0, minsize=0)
        self.frm.columnconfigure(1, weight=1, minsize=240)  # entry column expands
        self.frm.columnconfigure(0, minsize=150)
        self.frm.columnconfigure(2, minsize=110)

    def _set_column_weights_narrow(self):
        # single column, expand
        self.frm.columnconfigure(0, weight=1, minsize=260)

    # ---------- UI actions ----------

    def pick_inputs(self):
        paths = filedialog.askopenfilenames(
            title="選擇 IMU 原始檔（可多選）",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not paths:
            return
        self.in_paths = list(paths)
        first = os.path.basename(self.in_paths[0])
        more = len(self.in_paths) - 1
        self.in_path_disp.set(first + (f"  [+{more} 檔]" if more > 0 else ""))
        try:
            imu0 = load_imu_file(self.in_paths[0])
            self.fs_in_disp.set(f"{imu0.fs:.3f} Hz")
        except Exception:
            self.fs_in_disp.set("-")

    def pick_outdir(self):
        d = filedialog.askdirectory(title="選擇輸出資料夾")
        if d:
            self.out_dir.set(d)

    def run(self):
        if not self.in_paths:
            messagebox.showwarning("提醒", "請先選擇輸入檔案（可多選）")
            return
        out_dir = self.out_dir.get().strip()
        if not out_dir:
            messagebox.showwarning("提醒", "請選擇輸出資料夾")
            return

        try:
            fs_out = float(self.fs_out.get() or 0.0)
        except Exception:
            messagebox.showwarning("提醒", "請輸入有效的目標取樣頻率")
            return
        if fs_out <= 0:
            messagebox.showwarning("提醒", "目標取樣頻率必須大於 0")
            return

        method_map = {0: 'decimate', 1: 'mean', 2: 'linear'}
        method = method_map.get(int(self.method.get()), 'decimate')

        if method in ('decimate', 'mean'):
            violating = []
            for p in self.in_paths:
                try:
                    imu = load_imu_file(p)
                    if fs_out >= imu.fs:
                        violating.append(os.path.basename(p))
                except Exception:
                    pass
            if violating:
                names = "\n".join(violating[:6]) + ("\n..." if len(violating) > 6 else "")
                if messagebox.askyesno("確認",
                    "部分檔案的目標頻率 >= 原始頻率，這不是降取樣：\n"
                    f"{names}\n\n仍要繼續處理其餘檔案嗎？"
                ) is False:
                    return

        outputs: List[str] = []
        eff_fs_set: Set[float] = set()

        for in_path in self.in_paths:
            try:
                imu = load_imu_file(in_path)
            except Exception as e:
                messagebox.showerror("錯誤", f"讀取失敗：{in_path}\n{e}")
                continue

            try:
                new_lines = write_downsampled(imu, fs_out, method)
            except Exception as e:
                messagebox.showwarning("跳過", f"處理失敗（跳過）：{os.path.basename(in_path)}\n{e}")
                continue

            base = os.path.basename(in_path)
            out_path = os.path.join(out_dir, base)

            try:
                with open(out_path, 'w', encoding='utf-8', newline='') as f:
                    f.writelines(new_lines)
                outputs.append(out_path)
                if method in ('decimate', 'mean'):
                    import math
                    factor = max(1, int(round(imu.fs / fs_out)))
                    eff_fs_set.add(round(imu.fs / factor, 6))
                else:
                    eff_fs_set.add(round(fs_out, 6))
            except Exception as e:
                messagebox.showerror("錯誤", f"寫入失敗：{out_path}\n{e}")
                continue

        if not outputs:
            messagebox.showwarning("結果", "沒有成功輸出的檔案。")
            return

        eff_str = ", ".join(sorted({f"{v:.3f}Hz" for v in eff_fs_set}))
        messagebox.showinfo("完成",
            f"完成！共輸出 {len(outputs)} 個檔案至：\n{self.out_dir.get()}\n"
            f"實際輸出取樣頻率（可能依原始檔不同）：{eff_str}")

def main():
    root = Tk()
    try:
        style = ttk.Style(root)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
    except Exception:
        pass
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
