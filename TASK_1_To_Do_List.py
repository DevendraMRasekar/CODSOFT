import tkinter as tk
from tkinter import ttk, messagebox
import json, os, math
from datetime import datetime, date, timedelta

DATA_FILE = "todo_data.json"

BG       = "#0F0A1E"
PANEL    = "#1A1035"
CARD     = "#211545"
CARD2    = "#2A1B58"
PURPLE   = "#7C3AED"
PURPLE_M = "#8B5CF6"
PURPLE_L = "#A78BFA"
PURPLE_G = "#DDD6FE"
WHITE    = "#FFFFFF"
TEXT     = "#F5F3FF"
TEXT2    = "#C4B5FD"
MUTED    = "#7C6FAE"
BORDER   = "#3B2D6B"
GREEN    = "#10B981"
YELLOW   = "#F59E0B"
RED      = "#EF4444"
PINK     = "#EC4899"

DAYS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

PRIORITY_CFG = {
    "High":   {"bg":"#4C1C1C","fg":"#FCA5A5","dot":RED},
    "Medium": {"bg":"#44330A","fg":"#FDE68A","dot":YELLOW},
    "Low":    {"bg":"#064E3B","fg":"#6EE7B7","dot":GREEN},
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"tasks": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def date_key(d):
    return d.strftime("%Y-%m-%d")

def week_start(d):
    wd = d.weekday()          # Mon=0 … Sat=5, Sun=6
    return d if wd == 6 else d - timedelta(days=wd + 1)


def draw_ring(canvas, cx, cy, r, pct, thick=8, color=None):
    if color is None:
        color = PURPLE_M
    canvas.delete("all")
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=BORDER, width=thick)
    if pct > 0:
        ext = min(pct / 100 * 359.9, 359.9)
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                          start=90, extent=-ext,
                          outline=color, width=thick, style="arc")
    fs = max(int(r * 0.38), 8)
    canvas.create_text(cx, cy - 5, text=f"{int(pct)}%",
                       font=("Segoe UI", fs, "bold"), fill=WHITE)
    canvas.create_text(cx, cy + 8, text="done",
                       font=("Segoe UI", max(fs-4, 6)), fill=MUTED)


class AnalogClock(tk.Canvas):
    def __init__(self, parent, size=100, **kw):
        super().__init__(parent, width=size, height=size,
                         bg=PANEL, highlightthickness=0, **kw)
        self.cx = size // 2
        self.cy = size // 2
        self.r  = size // 2 - 5
        self._tick()

    def _tick(self):
        self._draw()
        self.after(1000, self._tick)

    def _draw(self):
        self.delete("all")
        cx, cy, r = self.cx, self.cy, self.r
        now = datetime.now()
        self.create_oval(cx-r, cy-r, cx+r, cy+r,
                         fill=CARD, outline=PURPLE, width=2)
        for i in range(12):
            ang  = math.radians(i * 30 - 90)
            is_q = (i % 3 == 0)
            r1   = r - 3 if is_q else r - 2
            r2   = r - 10 if is_q else r - 6
            self.create_line(cx + r1*math.cos(ang), cy + r1*math.sin(ang),
                             cx + r2*math.cos(ang), cy + r2*math.sin(ang),
                             fill=PURPLE_L if is_q else BORDER,
                             width=2 if is_q else 1)
        h = now.hour % 12
        m = now.minute
        s = now.second
        ha = math.radians((h + m/60) * 30 - 90)
        self.create_line(cx, cy,
                         cx+(r-22)*math.cos(ha), cy+(r-22)*math.sin(ha),
                         fill=WHITE, width=4, capstyle="round")
        ma = math.radians(m * 6 - 90)
        self.create_line(cx, cy,
                         cx+(r-14)*math.cos(ma), cy+(r-14)*math.sin(ma),
                         fill=PURPLE_G, width=3, capstyle="round")
        sa = math.radians(s * 6 - 90)
        self.create_line(cx, cy,
                         cx+(r-10)*math.cos(sa), cy+(r-10)*math.sin(sa),
                         fill=PINK, width=1, capstyle="round")
        self.create_oval(cx-3, cy-3, cx+3, cy+3,
                         fill=PURPLE, outline=WHITE, width=1)

class ToDoList:
    def __init__(self, root):
        self.root        = root
        self.root.title("TO DO LIST")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 620)
        self.root.configure(bg=BG)
        self.data        = load_data()
        self.today       = date.today()
        self.week_offset = 0
        self._build_ui()
        self.render()


    def _build_ui(self):

        hdr = tk.Frame(self.root, bg=PANEL)
        hdr.pack(fill="x")

        lh = tk.Frame(hdr, bg=PANEL)
        lh.pack(side="left", padx=20, pady=12)
        tk.Label(lh, text="✦  TO DO LIST",
                 font=("Segoe UI", 16, "bold"),
                 bg=PANEL, fg=WHITE).pack(side="left")


        cf = tk.Frame(hdr, bg=PANEL)
        cf.pack(side="left", expand=True)
        self.dtime = tk.Label(cf, text="",
                              font=("Courier New", 20, "bold"),
                              bg=PANEL, fg=PURPLE_L)
        self.dtime.pack()
        self.ddate = tk.Label(cf, text="",
                              font=("Segoe UI", 9),
                              bg=PANEL, fg=MUTED)
        self.ddate.pack()
        self._tick_clock()


        nav = tk.Frame(hdr, bg=PANEL)
        nav.pack(side="right", padx=16, pady=12)
        tk.Button(nav, text="◀", font=("Segoe UI", 10, "bold"),
                  bg=CARD2, fg=WHITE, relief="flat", cursor="hand2",
                  padx=10, pady=4,
                  command=lambda: self._shift(-1)).pack(side="left", padx=2)
        self.week_lbl = tk.Label(nav, text="",
                                 font=("Segoe UI", 9, "bold"),
                                 bg=PANEL, fg=TEXT2, width=24)
        self.week_lbl.pack(side="left", padx=6)
        tk.Button(nav, text="▶", font=("Segoe UI", 10, "bold"),
                  bg=CARD2, fg=WHITE, relief="flat", cursor="hand2",
                  padx=10, pady=4,
                  command=lambda: self._shift(1)).pack(side="left", padx=2)
        tk.Button(nav, text="Today", font=("Segoe UI", 9, "bold"),
                  bg=PURPLE, fg=WHITE, relief="flat", cursor="hand2",
                  padx=12, pady=4,
                  command=self._goto_today).pack(side="left", padx=8)


        tk.Frame(self.root, bg=PURPLE, height=2).pack(fill="x")


        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=12, pady=10)

        self.sidebar   = tk.Frame(body, bg=BG, width=250)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_propagate(False)

        self.week_area = tk.Frame(body, bg=BG)
        self.week_area.pack(side="left", fill="both", expand=True)


        bottom = tk.Frame(self.root, bg=PANEL, pady=10)
        bottom.pack(fill="x", side="bottom")
        tk.Button(bottom,
                  text="＋   ADD TASK",
                  font=("Segoe UI", 12, "bold"),
                  bg=PURPLE, fg=WHITE,
                  relief="flat", cursor="hand2",
                  padx=40, pady=10,
                  activebackground=PURPLE_M,
                  command=self._open_add_dialog
                  ).pack()


    def _tick_clock(self):
        now = datetime.now()
        self.dtime.config(text=now.strftime("%H : %M : %S"))
        self.ddate.config(text=now.strftime("%A, %d %B %Y"))
        self.root.after(1000, self._tick_clock)

    def _shift(self, d):
        self.week_offset += d
        self.render()

    def _goto_today(self):
        self.week_offset = 0
        self.render()

    def _week_days(self):
        base = self.today + timedelta(weeks=self.week_offset)
        ws   = week_start(base)
        return [ws + timedelta(days=i) for i in range(7)]


    def render(self):
        for w in self.sidebar.winfo_children():    w.destroy()
        for w in self.week_area.winfo_children():  w.destroy()
        days = self._week_days()
        self.week_lbl.config(
            text=f"{days[0].strftime('%d %b')}  –  {days[-1].strftime('%d %b %Y')}")
        self._build_sidebar(days)
        self._build_week(days)

    def _build_sidebar(self, days):

        cc = self._card(self.sidebar)
        cc.pack(fill="x", pady=(0, 8))
        row = tk.Frame(cc, bg=PANEL, padx=12, pady=12)
        row.pack(fill="x")
        AnalogClock(row, size=98).pack(side="left")

        sf = tk.Frame(row, bg=PANEL)
        sf.pack(side="left", padx=12, fill="y", expand=True)
        tk.Label(sf, text="This Week",
                 font=("Segoe UI", 9, "bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w")

        total_all = sum(len(self.data["tasks"].get(date_key(d), []))
                        for d in days)
        done_all  = sum(sum(1 for t in self.data["tasks"].get(date_key(d), [])
                            if t.get("done")) for d in days)

        for lbl, val, col in [
            ("Total",   total_all,            PURPLE_L),
            ("Done",    done_all,             GREEN),
            ("Pending", total_all - done_all, YELLOW),
        ]:
            r2 = tk.Frame(sf, bg=PANEL)
            r2.pack(anchor="w", pady=3)
            tk.Label(r2, text=str(val),
                     font=("Segoe UI", 14, "bold"),
                     bg=PANEL, fg=col).pack(side="left")
            tk.Label(r2, text=f"  {lbl}",
                     font=("Segoe UI", 8),
                     bg=PANEL, fg=MUTED).pack(side="left")

        bc = self._card(self.sidebar)
        bc.pack(fill="x", pady=(0, 8))
        tk.Label(bc, text="📊  Weekly Progress",
                 font=("Segoe UI", 10, "bold"),
                 bg=PANEL, fg=TEXT2).pack(anchor="w", padx=14, pady=(10, 4))
        chart = tk.Canvas(bc, bg=PANEL, height=85, highlightthickness=0)
        chart.pack(fill="x", padx=14, pady=(0, 10))

        def draw_chart(c=chart, ds=days):
            c.update_idletasks()
            W = c.winfo_width() or 215
            H = 78
            bw = max((W - 16) // 7 - 4, 6)
            for i, d in enumerate(ds):
                dk    = date_key(d)
                tasks = self.data["tasks"].get(dk, [])
                tot   = len(tasks)
                dn    = sum(1 for t in tasks if t.get("done"))
                p     = dn / tot if tot else 0
                bh    = max(int(p * (H - 18)), 3)
                x1    = 8 + i * (bw + 4)
                x2    = x1 + bw
                c.create_rectangle(x1, 4, x2, H - 14,
                                   fill=BORDER, outline="")
                if p > 0:
                    col = PURPLE if d == self.today else PURPLE_M
                    c.create_rectangle(x1, H-14-bh, x2, H-14,
                                       fill=col, outline="")
                lbl = DAYS[d.weekday() if d.weekday() != 6 else 6][:2]
                fc  = PURPLE_G if d == self.today else MUTED
                c.create_text(x1+bw//2, H-5, text=lbl,
                              font=("Segoe UI", 7, "bold"), fill=fc)

        bc.after(80, draw_chart)

        lc = self._card(self.sidebar)
        lc.pack(fill="both", expand=True)
        tk.Label(lc, text="📋  All Tasks This Week",
                 font=("Segoe UI", 10, "bold"),
                 bg=PANEL, fg=TEXT2).pack(anchor="w", padx=14, pady=(10, 4))

        canv  = tk.Canvas(lc, bg=PANEL, highlightthickness=0)
        sb    = ttk.Scrollbar(lc, orient="vertical", command=canv.yview)
        frame = tk.Frame(canv, bg=PANEL)
        frame.bind("<Configure>",
                   lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv.create_window((0, 0), window=frame, anchor="nw")
        canv.configure(yscrollcommand=sb.set)
        canv.pack(side="left", fill="both", expand=True, padx=6, pady=4)

        all_tasks = []
        for d in days:
            dk = date_key(d)
            for t in self.data["tasks"].get(dk, []):
                all_tasks.append((d, dk, t))

        if not all_tasks:
            tk.Label(frame, text="No tasks yet. Click ADD TASK!",
                     font=("Segoe UI", 8), bg=PANEL, fg=MUTED,
                     pady=10).pack()
        else:
            for d, dk, task in all_tasks:
                is_done = task.get("done", False)
                p       = PRIORITY_CFG[task.get("priority", "Medium")]
                row3    = tk.Frame(frame, bg=CARD2, pady=3, padx=8)
                row3.pack(fill="x", pady=1)
                tk.Label(row3, text="●",
                         font=("Segoe UI", 8),
                         bg=CARD2, fg=p["dot"]).pack(side="left")
                style = ("Segoe UI", 8, "overstrike") if is_done \
                        else ("Segoe UI", 8)
                tk.Label(row3,
                         text=f"{task['title'][:14]}  "
                              f"[{DAYS[d.weekday() if d.weekday()!=6 else 6]}]",
                         font=style, bg=CARD2,
                         fg=MUTED if is_done else TEXT2,
                         anchor="w").pack(side="left")

    def _build_week(self, days):
        for i, d in enumerate(days):
            self._day_col(self.week_area, d, i)

    def _day_col(self, parent, d, col_i):
        dk       = date_key(d)
        is_today = (d == self.today)
        tasks    = self.data["tasks"].get(dk, [])
        total    = len(tasks)
        done     = sum(1 for t in tasks if t.get("done"))
        pct      = done / total * 100 if total else 0

        col = tk.Frame(parent, bg=BG)
        col.grid(row=0, column=col_i, sticky="nsew", padx=3)
        parent.columnconfigure(col_i, weight=1)
        parent.rowconfigure(0, weight=1)

        hbg = PURPLE if is_today else CARD
        hbd = PURPLE if is_today else BORDER
        hcard = tk.Frame(col, bg=hbg,
                         highlightthickness=2,
                         highlightbackground=hbd)
        hcard.pack(fill="x")
        tk.Label(hcard,
                 text=DAYS[d.weekday() if d.weekday() != 6 else 6],
                 font=("Segoe UI", 10, "bold"),
                 bg=hbg,
                 fg=WHITE if is_today else TEXT2).pack(pady=(7, 0))
        tk.Label(hcard, text=d.strftime("%d.%m"),
                 font=("Segoe UI", 8),
                 bg=hbg,
                 fg=PURPLE_G if is_today else MUTED).pack(pady=(0, 7))

        rc     = PURPLE if is_today else PURPLE_M
        ring_c = tk.Canvas(col, bg=BG, width=68, height=68,
                           highlightthickness=0)
        ring_c.pack(pady=4)
        col.after(60 + col_i * 10,
                  lambda c=ring_c, p=pct, color=rc:
                  draw_ring(c, 34, 34, 26, p, 7, color))

        tk.Label(col,
                 text=f"{done}/{total} tasks" if total else "No tasks",
                 font=("Segoe UI", 7),
                 bg=BG,
                 fg=PURPLE_L if total else MUTED).pack()

        outer = tk.Frame(col, bg=BG)
        outer.pack(fill="both", expand=True, pady=4)

        canv = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb   = ttk.Scrollbar(outer, orient="vertical", command=canv.yview)
        tf   = tk.Frame(canv, bg=BG)
        tf.bind("<Configure>",
                lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv.create_window((0, 0), window=tf, anchor="nw")
        canv.configure(yscrollcommand=sb.set)
        canv.pack(side="left", fill="both", expand=True)

        def _sc(e, c=canv):
            c.yview_scroll(-1*(e.delta//120), "units")
        canv.bind("<MouseWheel>", _sc)
        tf.bind("<MouseWheel>", _sc)

        if not tasks:
            tk.Label(tf, text="Empty",
                     font=("Segoe UI", 7),
                     bg=BG, fg=MUTED, pady=4).pack()
        for task in tasks:
            self._task_card(tf, task, dk)

    def _task_card(self, parent, task, dk):
        priority = task.get("priority", "Medium")
        pcfg     = PRIORITY_CFG[priority]
        is_done  = task.get("done", False)

        outer = tk.Frame(parent, bg=pcfg["dot"])
        outer.pack(fill="x", pady=2, padx=2)
        inner = tk.Frame(outer, bg=CARD, padx=6, pady=5)
        inner.pack(fill="x", padx=(3, 0))

        row = tk.Frame(inner, bg=CARD)
        row.pack(fill="x")

        var = tk.BooleanVar(value=is_done)

        def _tog(t=task, v=var, k=dk):
            t["done"] = v.get()
            save_data(self.data)
            self.render()

        tk.Checkbutton(row, variable=var, bg=CARD,
                       selectcolor=PURPLE, activebackground=CARD,
                       cursor="hand2", command=_tog).pack(side="left")

        style = ("Segoe UI", 8, "overstrike") if is_done \
                else ("Segoe UI", 8, "bold")
        tk.Label(row, text=task.get("title", "")[:16],
                 font=style, bg=CARD,
                 fg=MUTED if is_done else TEXT,
                 anchor="w").pack(side="left", fill="x", expand=True)

        tk.Button(row, text="✕",
                  font=("Segoe UI", 7),
                  bg=CARD, fg=RED, relief="flat", cursor="hand2",
                  activebackground=CARD,
                  command=lambda t=task, k=dk: self._del(t, k)
                  ).pack(side="right")

        pb = tk.Frame(inner, bg=CARD)
        pb.pack(anchor="w", pady=(2, 0))
        tk.Label(pb, text=f"● {priority}",
                 font=("Segoe UI", 6, "bold"),
                 bg=pcfg["bg"], fg=pcfg["fg"],
                 padx=4, pady=1).pack(side="left")

    def _open_add_dialog(self):
        days = self._week_days()

        dlg = tk.Toplevel(self.root)
        dlg.title("Add Task")
        dlg.geometry("420x400")
        dlg.configure(bg=PANEL)
        dlg.resizable(False, False)
        dlg.transient(self.root)   # stay above main window
        dlg.grab_set()             # block main window
        dlg.focus_force()          # bring to front

        dlg.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - 420) // 2
        y  = (sh - 400) // 2
        dlg.geometry(f"420x400+{x}+{y}")

        tk.Frame(dlg, bg=PURPLE, pady=12).pack(fill="x")
        tk.Label(dlg.winfo_children()[-1],
                 text="✦   ADD NEW TASK",
                 font=("Segoe UI", 13, "bold"),
                 bg=PURPLE, fg=WHITE).pack()

        form = tk.Frame(dlg, bg=PANEL)
        form.pack(fill="both", expand=True, padx=24, pady=10)

        tk.Label(form, text="Task Title  *",
                 font=("Segoe UI", 10),
                 bg=PANEL, fg=TEXT2, anchor="w").pack(fill="x", pady=(8, 2))

        title_var = tk.StringVar()
        title_entry = tk.Entry(form,
                               textvariable=title_var,
                               font=("Segoe UI", 11),
                               bg="#2A1B58",
                               fg="#FFFFFF",
                               insertbackground="#FFFFFF",
                               relief="solid",
                               bd=1)
        title_entry.pack(fill="x", ipady=8)
        title_entry.focus_set()

        tk.Label(form, text="Select Day  *",
                 font=("Segoe UI", 10),
                 bg=PANEL, fg=TEXT2, anchor="w").pack(fill="x", pady=(12, 4))

        selected_day = [0]
        for i, d in enumerate(days):
            if d == self.today:
                selected_day[0] = i
                break

        day_btns = []
        day_row  = tk.Frame(form, bg=PANEL)
        day_row.pack(fill="x")

        def select_day(idx):
            selected_day[0] = idx
            for j, btn in enumerate(day_btns):
                if j == idx:
                    btn.config(bg=PURPLE, fg=WHITE)
                else:
                    btn.config(bg=CARD2, fg=MUTED)

        for i, d in enumerate(days):
            name = DAYS[d.weekday() if d.weekday() != 6 else 6][:3]
            num  = d.strftime("%d")
            btn  = tk.Button(day_row,
                             text=f"{name}\n{num}",
                             font=("Segoe UI", 8, "bold"),
                             bg=PURPLE if i == selected_day[0] else CARD2,
                             fg=WHITE  if i == selected_day[0] else MUTED,
                             relief="flat", cursor="hand2",
                             width=4, pady=5,
                             activebackground=PURPLE_M,
                             command=lambda idx=i: select_day(idx))
            btn.pack(side="left", padx=2)
            day_btns.append(btn)

        tk.Label(form, text="Priority",
                 font=("Segoe UI", 10),
                 bg=PANEL, fg=TEXT2, anchor="w").pack(fill="x", pady=(12, 4))

        pvar = tk.StringVar(value="Medium")
        prow = tk.Frame(form, bg=PANEL)
        prow.pack(anchor="w")
        for p in ["High", "Medium", "Low"]:
            pc = PRIORITY_CFG[p]
            tk.Radiobutton(prow, text=p, variable=pvar, value=p,
                           font=("Segoe UI", 9, "bold"),
                           bg=PANEL, fg=pc["dot"],
                           selectcolor=PANEL,
                           activebackground=PANEL,
                           cursor="hand2").pack(side="left", padx=10)

        def save():
            t = title_var.get().strip()
            if not t:
                messagebox.showwarning("Missing",
                                       "Please type a task title!",
                                       parent=dlg)
                title_entry.focus_set()
                return
            dk = date_key(days[selected_day[0]])
            self.data["tasks"].setdefault(dk, []).append({
                "title":    t,
                "done":     False,
                "priority": pvar.get(),
                "created":  date.today().isoformat()
            })
            save_data(self.data)
            self.render()
            dlg.destroy()

        tk.Button(form, text="✓   Save Task",
                  font=("Segoe UI", 11, "bold"),
                  bg=PURPLE, fg=WHITE,
                  relief="flat", cursor="hand2",
                  pady=10,
                  activebackground=PURPLE_M,
                  command=save).pack(fill="x", pady=16)

        dlg.bind("<Return>", lambda e: save())
        dlg.wait_window()

    def _del(self, task, dk):
        if messagebox.askyesno("Delete",
                               f"Delete '{task['title']}'?",
                               icon="warning"):
            lst = self.data["tasks"].get(dk, [])
            if task in lst:
                lst.remove(task)
                save_data(self.data)
                self.render()

    def _card(self, parent):
        return tk.Frame(parent, bg=PANEL,
                        highlightthickness=1,
                        highlightbackground=BORDER)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.1)
    except:
        pass
    ToDoList(root)
    root.mainloop()