import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import date, datetime
from difflib import SequenceMatcher
import re
import csv
import io
import zipfile
# ---------------- DATABASE ---------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MYSQL password",
    "database": "my_memory"
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
# ---------------- COLORS ----------------
NAVY = "#172554"
NAVY_LIGHT = "#243765"
BLUE = "#2563EB"
BG = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
# ---------------- TABLE DETAILS ----------------
TABLES = {
    "Subjects": {
        "table": "subjects",
        "columns": ["sub_id", "sub_name"],
        "fields": [
            ("sub_name", "Subject Name", "entry", True)
        ]
    },
    "Topics": {
        "table": "topics",
        "columns": [
            "topic_id", "sub_id", "topic_name",
            "computer_definationa", "my_defination"
        ],
        "fields": [
            ("sub_id", "Subject", "subject", True),
            ("topic_name", "Topic Name", "entry", True),
            ("computer_definationa", "Computer Definition", "entry", True),
            ("my_defination", "My Definition", "entry", True)
        ]
    },
    "Company": {
        "table": "company",
        "columns": ["comp_id", "comp_name", "location"],
        "fields": [
            ("comp_name", "Company Name", "entry", True),
            ("location", "Location", "entry", False)
        ]
    },
    "Interview": {
        "table": "interview",
        "columns": [
            "interview_id", "job_role", "inteview_date",
            "rounds", "comp_id"
        ],
        "fields": [
            ("job_role", "Job Role", "entry", False),
            ("inteview_date", "Interview Date (YYYY-MM-DD)", "entry", False),
            ("rounds", "Number of Rounds", "entry", False),
            ("comp_id", "Company", "company", False)
        ]
    },
    "Interview Questions": {
        "table": "inter_questions",
        "columns": [
            "question_no", "question", "question_type", "interview_id",
            "answer", "practice_status", "confidence_level", "last_practiced"
        ],
        "fields": [
            ("question", "Question", "text", True),
            ("answer", "Expected Answer", "text", False),
            ("question_type", "Question Type", "entry", False),
            ("interview_id", "Interview", "interview", False)
        ]
    }
}
# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("My Memory | Interview Preparation")
root.geometry("1200x760")
root.minsize(950, 600)
root.configure(bg=BG)
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TFrame",
    background=BG
)
style.configure(
    "Card.TFrame",
    background=WHITE
)
style.configure(
    "TLabel",
    background=BG,
    foreground=TEXT,
    font=("Segoe UI", 10)
)
style.configure(
    "Title.TLabel",
    background=BG,
    foreground=NAVY,
    font=("Segoe UI", 22, "bold")
)
style.configure(
    "Subtitle.TLabel",
    background=BG,
    foreground=MUTED,
    font=("Segoe UI", 10)
)
style.configure(
    "CardTitle.TLabel",
    background=WHITE,
    foreground=NAVY,
    font=("Segoe UI", 13, "bold")
)
style.configure(
    "Field.TLabel",
    background=WHITE,
    foreground=TEXT,
    font=("Segoe UI", 10, "bold")
)
style.configure(
    "TEntry",
    padding=8,
    fieldbackground=WHITE,
    foreground=TEXT
)
style.configure(
    "TCombobox",
    padding=7,
    fieldbackground=WHITE,
    foreground=TEXT
)
style.configure(
    "Primary.TButton",
    background=BLUE,
    foreground=WHITE,
    padding=(16, 9),
    font=("Segoe UI", 10, "bold"),
    borderwidth=0
)
style.map(
    "Primary.TButton",
    background=[("active", "#1D4ED8")]
)
style.configure(
    "Secondary.TButton",
    background="#E8EEF9",
    foreground=NAVY,
    padding=(14, 9),
    font=("Segoe UI", 10),
    borderwidth=0
)
style.map(
    "Secondary.TButton",
    background=[("active", "#D8E3F5")]
)
style.configure(
    "Treeview",
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT,
    rowheight=40,
    font=("Segoe UI", 10),
    borderwidth=0
)
style.configure(
    "Treeview.Heading",
    background="#EAF0FA",
    foreground=NAVY,
    font=("Segoe UI", 9, "bold"),
    padding=9,
    relief="flat"
)
style.map(
    "Treeview",
    background=[("selected", "#DCE8FF")],
    foreground=[("selected", NAVY)]
)
# ---------------- APPLICATION LAYOUT ----------------
shell = tk.Frame(root, bg=BG)
shell.pack(fill="both", expand=True)
sidebar = tk.Frame(shell, bg=NAVY, width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
main = tk.Frame(shell, bg=BG)
main.pack(side="left", fill="both", expand=True)
# Sidebar brand
brand = tk.Frame(sidebar, bg=NAVY)
brand.pack(fill="x", padx=20, pady=(25, 30))
tk.Label(
    brand,
    text="MY MEMORY",
    bg=NAVY,
    fg=WHITE,
    font=("Segoe UI", 19, "bold")
).pack(anchor="w")
tk.Label(
    brand,
    text="INTERVIEW PREPARATION",
    bg=NAVY,
    fg="#AFC5F8",
    font=("Segoe UI", 8, "bold")
).pack(anchor="w", pady=(5, 0))
tk.Label(
    sidebar,
    text="WORKSPACE",
    bg=NAVY,
    fg="#91A6D0",
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", padx=20, pady=(0, 10))
# Main header
header = tk.Frame(main, bg=WHITE, height=76)
header.pack(fill="x")
header.pack_propagate(False)
header_left = tk.Frame(header, bg=WHITE)
header_left.pack(side="left", padx=28, pady=12)
page_title = tk.Label(
    header_left,
    text="Dashboard",
    bg=WHITE,
    fg=NAVY,
    font=("Segoe UI", 17, "bold")
)
page_title.pack(anchor="w")
page_subtitle = tk.Label(
    header_left,
    text="Organize your learning and interview preparation",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9)
)
page_subtitle.pack(anchor="w", pady=(2, 0))
content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True, padx=25, pady=22)
# ---------------- FORM STORAGE ----------------
forms = {}
sort_states = {}
pages = {}
nav_buttons = {}
current_page = None
# ---------------- FOREIGN KEY OPTIONS ----------------
def get_dropdown_options(kind):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        if kind == "subject":
            cursor.execute(
                "SELECT sub_id, sub_name FROM subjects ORDER BY sub_id"
            )
        elif kind == "company":
            cursor.execute(
                "SELECT comp_id, comp_name FROM company ORDER BY comp_id"
            )
        elif kind == "interview":
            cursor.execute(
                "SELECT interview_id, job_role "
                "FROM interview ORDER BY interview_id"
            )
        records = cursor.fetchall()
        return [
            f"{record[0]} - {record[1] or '(No name)'}"
            for record in records
        ]
    finally:
        cursor.close()
        connection.close()
def refresh_dropdowns():
    for form in forms.values():
        for field_name, widget in form["widgets"].items():
            if field_name == "sub_id":
                kind = "subject"
            elif field_name == "comp_id":
                kind = "company"
            elif field_name == "interview_id":
                kind = "interview"
            else:
                continue
            old_value = widget.get()
            try:
                options = get_dropdown_options(kind)
                widget["values"] = options
                if old_value in options:
                    widget.set(old_value)
                elif old_value:
                    widget.set("")
            except mysql.connector.Error:
                widget["values"] = ()
# ---------------- RECORD TABLE ----------------
def refresh_records(tab_name):
    """Load records from MySQL, optionally matching this page's search text."""
    form = forms[tab_name]
    config = TABLES[tab_name]
    search_text = form["search_var"].get().strip()
    # Include related subject/company/interview names, not only foreign-key IDs.
    search_config = {
        "Subjects": ("SELECT s.* FROM subjects s", ["s.sub_id", "s.sub_name"]),
        "Topics": (
            "SELECT t.* FROM topics t LEFT JOIN subjects s ON t.sub_id = s.sub_id",
            ["t.topic_id", "s.sub_name", "t.topic_name", "t.computer_definationa", "t.my_defination"],
        ),
        "Company": ("SELECT c.* FROM company c", ["c.comp_id", "c.comp_name", "c.location"]),
        "Interview": (
            "SELECT i.* FROM interview i LEFT JOIN company c ON i.comp_id = c.comp_id",
            ["i.interview_id", "i.job_role", "i.inteview_date", "i.rounds", "c.comp_name", "c.location"],
        ),
        "Interview Questions": (
            "SELECT q.* FROM inter_questions q "
            "LEFT JOIN interview i ON q.interview_id = i.interview_id "
            "LEFT JOIN company c ON i.comp_id = c.comp_id",
            ["q.question_no", "q.question", "q.question_type", "i.job_role", "c.comp_name"],
        ),
    }
    base_query, searchable_columns = search_config[tab_name]
    query = base_query
    params = ()
    if search_text:
        conditions = " OR ".join(
            f"CAST({column} AS CHAR) LIKE %s" for column in searchable_columns
        )
        query += " WHERE " + conditions
        params = tuple(f"%{search_text}%" for _ in searchable_columns)
    query += f" ORDER BY {config['columns'][0]} DESC"
    try:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                records = cursor.fetchall()
                form["tree"].delete(*form["tree"].get_children())
                for record in records:
                    display_record = list(record)
                    if tab_name == "Interview Questions" and len(display_record) > 1:
                        if not str(display_record[1] or "").strip():
                            display_record[1] = "⚠ Missing question — edit this record"
                    form["tree"].insert("", "end", values=display_record)
                if form.get("record_count"):
                    form["record_count"].config(
                        text=f"{len(records)} record{'s' if len(records) != 1 else ''}"
                    )
            finally:
                cursor.close()
        finally:
            connection.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))
def sort_table(tab_name, column):
    """Sort the currently displayed rows by clicking a column heading."""
    form = forms[tab_name]
    tree = form["tree"]
    columns = list(tree["columns"])
    column_index = columns.index(column)
    state = sort_states.setdefault(tab_name, {"column": None, "reverse": False})

    if state["column"] == column:
        state["reverse"] = not state["reverse"]
    else:
        state["column"] = column
        state["reverse"] = False

    rows = []
    for item in tree.get_children(""):
        values = tree.item(item, "values")
        value = values[column_index] if column_index < len(values) else ""
        text_value = "" if value is None else str(value)
        try:
            sort_key = (0, float(text_value))
        except (ValueError, TypeError):
            sort_key = (1, text_value.casefold())
        rows.append((sort_key, item))

    rows.sort(key=lambda pair: pair[0], reverse=state["reverse"])
    for position, (_, item) in enumerate(rows):
        tree.move(item, "", position)

    # Show the current sort direction in the active column heading.
    for name in columns:
        heading = name.replace("_", " ").title()
        if name == column:
            heading += "  ▼" if state["reverse"] else "  ▲"
        tree.heading(name, text=heading)


def show_record_details(tab_name):
    """Show selected data in a readable detail window; compare topic definitions side by side."""
    form = forms[tab_name]
    tree = form["tree"]
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Select a Record", "Please select a row in the table first.")
        return

    values = tree.item(selected[0], "values")
    columns = TABLES[tab_name]["columns"]

    detail_window = tk.Toplevel(root)
    detail_window.title(f"{tab_name} - Full Details")
    detail_window.geometry("1000x650" if tab_name == "Topics" else "820x620")
    detail_window.minsize(650, 420)
    detail_window.configure(bg=BG)
    detail_window.transient(root)

    tk.Label(
        detail_window,
        text=f"{tab_name} — Full Details",
        bg=BG, fg=NAVY, font=("Segoe UI", 17, "bold")
    ).pack(anchor="w", padx=22, pady=(18, 4))

    if tab_name == "Topics":
        # Topic table order: topic_id, sub_id, topic_name, computer definition, own definition.
        topic_name = str(values[2]) if len(values) > 2 and values[2] is not None else "Untitled topic"
        computer_definition = str(values[3]) if len(values) > 3 and values[3] is not None else ""
        own_definition = str(values[4]) if len(values) > 4 and values[4] is not None else ""
        tk.Label(
            detail_window, text=topic_name, bg=BG, fg=TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 12))

        compare_frame = tk.Frame(detail_window, bg=BG)
        compare_frame.pack(fill="both", expand=True, padx=22, pady=(0, 14))
        compare_frame.columnconfigure(0, weight=1, uniform="definition")
        compare_frame.columnconfigure(1, weight=1, uniform="definition")
        compare_frame.rowconfigure(0, weight=1)

        def add_definition_panel(parent, title, content, column):
            panel = tk.Frame(parent, bg=WHITE, highlightbackground="#DCE4F0", highlightthickness=1)
            panel.grid(row=0, column=column, sticky="nsew", padx=(0, 8) if column == 0 else (8, 0))
            tk.Label(
                panel, text=title, bg=WHITE, fg=NAVY,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", padx=14, pady=(14, 8))
            text_frame = tk.Frame(panel, bg=WHITE)
            text_frame.pack(fill="both", expand=True, padx=12)
            text_widget = tk.Text(
                text_frame, wrap="word", font=("Segoe UI", 11), bg="#FBFCFF",
                fg=TEXT, relief="flat", padx=12, pady=12,
                spacing1=2, spacing3=6, height=12
            )
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            text_widget.insert("1.0", content if content.strip() else "No definition saved yet.")
            text_widget.configure(state="disabled")

            def copy_definition(text=content, button_title=title):
                detail_window.clipboard_clear()
                detail_window.clipboard_append(text)
                detail_window.update_idletasks()
                messagebox.showinfo("Copied", f"{button_title} copied to clipboard.", parent=detail_window)

            ttk.Button(
                panel, text="Copy Definition", style="Secondary.TButton",
                command=copy_definition
            ).pack(anchor="e", padx=12, pady=12)

        add_definition_panel(compare_frame, "Computer Definition", computer_definition, 0)
        add_definition_panel(compare_frame, "My Definition", own_definition, 1)
    else:
        tk.Label(
            detail_window,
            text="The complete content is shown below with text wrapping.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", padx=22, pady=(0, 12))

        body = tk.Frame(detail_window, bg=WHITE, highlightbackground="#E2E8F0", highlightthickness=1)
        body.pack(fill="both", expand=True, padx=22, pady=(0, 16))
        details_text = tk.Text(
            body, wrap="word", font=("Segoe UI", 11), bg=WHITE, fg=TEXT,
            relief="flat", padx=16, pady=14, spacing1=3, spacing3=8,
            state="normal"
        )
        scroll = ttk.Scrollbar(body, orient="vertical", command=details_text.yview)
        details_text.configure(yscrollcommand=scroll.set)
        details_text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        details_text.tag_configure("field", font=("Segoe UI", 10, "bold"), foreground=BLUE, spacing1=8)

        for column, value in zip(columns, values):
            details_text.insert("end", column.replace("_", " ").title() + "\n", "field")
            details_text.insert("end", (str(value) if value is not None else "—") + "\n\n")
        details_text.configure(state="disabled")

    ttk.Button(
        detail_window, text="Close", style="Secondary.TButton",
        command=detail_window.destroy
    ).pack(anchor="e", padx=22, pady=(0, 18))

def clear_search(tab_name):
    """Clear search and display all records again."""
    forms[tab_name]["search_var"].set("")
    refresh_records(tab_name)
def refresh_dashboard_stats(show_errors=False):
    """Refresh dashboard totals and practice status directly from MySQL."""
    table_queries = {
        "subjects": "SELECT COUNT(*) FROM subjects",
        "topics": "SELECT COUNT(*) FROM topics",
        "companies": "SELECT COUNT(*) FROM company",
        "interviews": "SELECT COUNT(*) FROM interview",
        "questions": "SELECT COUNT(*) FROM inter_questions WHERE question IS NOT NULL AND TRIM(question) <> ''",
    }
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            for key, query in table_queries.items():
                cursor.execute(query)
                count = cursor.fetchone()[0]
                if key in dashboard_stats:
                    dashboard_stats[key].config(text=str(count))
            cursor.execute(
                "SELECT COALESCE(SUM(CASE WHEN practice_status = 'Got it' THEN 1 ELSE 0 END), 0), "
                "COALESCE(SUM(CASE WHEN practice_status = 'Need revision' THEN 1 ELSE 0 END), 0), "
                "COALESCE(SUM(CASE WHEN practice_status IS NULL OR practice_status = 'Not Started' OR TRIM(practice_status) = '' THEN 1 ELSE 0 END), 0) "
                "FROM inter_questions WHERE question IS NOT NULL AND TRIM(question) <> ''"
            )
            got_it, revision, not_started = cursor.fetchone()
            total = int(got_it or 0) + int(revision or 0) + int(not_started or 0)
            if total:
                percent = round((int(got_it or 0) / total) * 100)
                practice_progress_label.config(
                    text=f"{got_it} mastered  •  {revision} need revision  •  {not_started} not started"
                )
                progress_percent_label.config(text=f"{percent}%")
                draw_progress_bar(percent)
            else:
                practice_progress_label.config(text="No valid interview questions yet. Add questions to start tracking your progress.")
                progress_percent_label.config(text="0%")
                draw_progress_bar(0)
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        for label in dashboard_stats.values():
            label.config(text="—")
        practice_progress_label.config(text="Dashboard statistics could not be loaded. Check your MySQL connection.")
        progress_percent_label.config(text="—")
        draw_progress_bar(0)
        if show_errors:
            messagebox.showerror("Dashboard Refresh Failed", str(error), parent=root)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

def export_all_data():
    """Save every app table to a ZIP containing separate UTF-8 CSV files."""
    destination = filedialog.asksaveasfilename(
        parent=root, title="Export My Memory data",
        defaultextension=".zip",
        initialfile=f"my_memory_backup_{date.today().isoformat()}.zip",
        filetypes=[("ZIP archive", "*.zip")]
    )
    if not destination:
        return
    tables = ["subjects", "topics", "company", "interview", "inter_questions"]
    connection = None
    try:
        connection = get_connection()
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            cursor = connection.cursor()
            try:
                for table_name in tables:
                    cursor.execute(f"SELECT * FROM `{table_name}`")
                    headers = [column[0] for column in cursor.description]
                    output = io.StringIO(newline="")
                    writer = csv.writer(output)
                    writer.writerow(headers)
                    for record in cursor.fetchall():
                        writer.writerow([
                            value.isoformat() if hasattr(value, "isoformat") else value
                            for value in record
                        ])
                    archive.writestr(f"{table_name}.csv", output.getvalue().encode("utf-8-sig"))
            finally:
                cursor.close()
        messagebox.showinfo(
            "Export Complete",
            "All five My Memory tables were exported to the selected ZIP file. Keep this backup somewhere safe.",
            parent=root
        )
    except (mysql.connector.Error, OSError, zipfile.BadZipFile) as error:
        messagebox.showerror("Export Failed", str(error), parent=root)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

def refresh_all():
    refresh_dropdowns()
    for tab_name in forms:
        refresh_records(tab_name)
    refresh_dashboard_stats(show_errors=False)
# ---------------- CLEAR FORM ----------------
def clear_form(tab_name):
    for widget in forms[tab_name]["widgets"].values():
        if isinstance(widget, ttk.Combobox):
            widget.set("")
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", "end")
        else:
            widget.delete(0, tk.END)
# ---------------- SAVE RECORD ----------------
def save_record(tab_name):
    config = TABLES[tab_name]
    form = forms[tab_name]
    values = {}
    for field_name, label, field_type, required in config["fields"]:
        widget = form["widgets"][field_name]
        if isinstance(widget, tk.Text):
            value = widget.get("1.0", "end-1c").strip()
        else:
            value = widget.get().strip()
        if field_type in ("subject", "company", "interview"):
            if value:
                value = value.split(" - ", 1)[0]
            else:
                value = None
        elif value == "":
            value = None
        if required and value is None:
            messagebox.showwarning(
                "Missing Information",
                f"Please enter or select {label}."
            )
            return
        values[field_name] = value
    # Validate rounds
    if values.get("rounds") is not None:
        try:
            values["rounds"] = int(values["rounds"])
            if values["rounds"] < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Number of rounds must be a non-negative whole number."
            )
            return
    # Validate interview date
    if values.get("inteview_date"):
        try:
            date.fromisoformat(values["inteview_date"])
        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Enter the date in YYYY-MM-DD format."
            )
            return
    # Do not allow an entirely blank interview record. The Interview form has
    # optional fields, so require at least a role or a linked company.
    if tab_name == "Interview" and not any(
        values.get(field) for field in ("job_role", "inteview_date", "rounds", "comp_id")
    ):
        messagebox.showwarning(
            "Missing Information",
            "Enter at least a job role, interview date, number of rounds, or select a company."
        )
        return

    # Prevent accidentally saving the same question more than once for the
    # same interview. A question is required above; expected answer stays optional.
    if tab_name == "Interview Questions":
        question_text = (values.get("question") or "").strip()
        interview_id = values.get("interview_id")
        try:
            connection = get_connection()
            try:
                cursor = connection.cursor()
                try:
                    if interview_id is None:
                        cursor.execute(
                            "SELECT question_no FROM inter_questions "
                            "WHERE LOWER(TRIM(question)) = LOWER(TRIM(%s)) "
                            "AND interview_id IS NULL LIMIT 1",
                            (question_text,)
                        )
                    else:
                        cursor.execute(
                            "SELECT question_no FROM inter_questions "
                            "WHERE LOWER(TRIM(question)) = LOWER(TRIM(%s)) "
                            "AND interview_id = %s LIMIT 1",
                            (question_text, interview_id)
                        )
                    duplicate = cursor.fetchone()
                finally:
                    cursor.close()
            finally:
                connection.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Could Not Check Duplicate", str(error), parent=root)
            return
        if duplicate:
            messagebox.showwarning(
                "Duplicate Question",
                "This question already exists for the selected interview. "
                "Open the existing record and edit it instead of saving a duplicate.",
                parent=root
            )
            return

    columns = list(values.keys())
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(f"`{column}`" for column in columns)
    query = (
        f"INSERT INTO `{config['table']}` "
        f"({column_names}) VALUES ({placeholders})"
    )
    try:
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, tuple(values.values()))
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
        clear_form(tab_name)
        refresh_all()
        messagebox.showinfo(
            "Saved Successfully",
            f"{tab_name} record has been saved."
        )
    except mysql.connector.Error as error:
        messagebox.showerror("Could Not Save Record", str(error))
# ---------------- NAVIGATION ----------------
def show_page(tab_name):
    global current_page
    # Preserve the typed answer when leaving Practice Mode.
    if current_page == "Practice Mode" and tab_name != "Practice Mode":
        save_current_practice_draft()
    if current_page is not None:
        pages[current_page].pack_forget()
    pages[tab_name].pack(fill="both", expand=True)
    current_page = tab_name
    # Always reload from MySQL when Practice Mode is opened so new, edited,
    # or deleted questions are reflected immediately.
    if tab_name == "Practice Mode":
        load_practice_questions()
        practice_canvas.configure(scrollregion=practice_canvas.bbox("all"))
        practice_canvas.yview_moveto(0)
        root.after_idle(lambda: _install_mousewheel_tag(practice_page))
    page_title.config(text=tab_name)
    if tab_name == "Dashboard":
        page_subtitle.config(
            text="Your interview preparation workspace"
        )
    else:
        page_subtitle.config(
            text=("Practise saved interview questions and track revision" if tab_name == "Practice Mode"
                  else f"Create and review your {tab_name.lower()} records")
        )
    for name, button in nav_buttons.items():
        if name == tab_name:
            button.config(
                bg=BLUE,
                fg=WHITE,
                activebackground=BLUE,
                activeforeground=WHITE
            )
        else:
            button.config(
                bg=NAVY,
                fg="#D5DFF5",
                activebackground=NAVY_LIGHT,
                activeforeground=WHITE
            )
def create_nav_button(name, symbol):
    button = tk.Button(
        sidebar,
        text=f"  {symbol}   {name}",
        anchor="w",
        font=("Segoe UI", 10, "bold"),
        bg=NAVY,
        fg="#D5DFF5",
        activebackground=NAVY_LIGHT,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=14,
        pady=12,
        cursor="hand2",
        command=lambda: show_page(name)
    )
    button.pack(fill="x", padx=10, pady=2)
    nav_buttons[name] = button
# ---------------- DASHBOARD ----------------
dashboard_shell = tk.Frame(content, bg=BG)
pages["Dashboard"] = dashboard_shell
dashboard_canvas = tk.Canvas(dashboard_shell, bg=BG, highlightthickness=0, bd=0)
dashboard_scrollbar = ttk.Scrollbar(dashboard_shell, orient="vertical", command=dashboard_canvas.yview)
dashboard_canvas.configure(yscrollcommand=dashboard_scrollbar.set)
dashboard_scrollbar.pack(side="right", fill="y")
dashboard_canvas.pack(side="left", fill="both", expand=True)
dashboard = tk.Frame(dashboard_canvas, bg=BG, padx=24, pady=22)
dashboard_window = dashboard_canvas.create_window((0, 0), window=dashboard, anchor="nw")
def _dashboard_content_resized(event=None):
    dashboard_canvas.configure(scrollregion=dashboard_canvas.bbox("all"))
def _dashboard_canvas_resized(event):
    dashboard_canvas.itemconfigure(dashboard_window, width=event.width)
def _dashboard_mousewheel(event):
    dashboard_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
dashboard.bind("<Configure>", _dashboard_content_resized)
dashboard_canvas.bind("<Configure>", _dashboard_canvas_resized)

# Welcome header: clear title, short purpose, and one primary action.
hero = tk.Frame(dashboard, bg=NAVY, padx=28, pady=24)
hero.pack(fill="x", pady=(0, 22))
hero.columnconfigure(0, weight=1)
hero_left = tk.Frame(hero, bg=NAVY)
hero_left.grid(row=0, column=0, sticky="ew")
tk.Label(hero_left, text="MY MEMORY", bg=NAVY, fg="#AFC7FF",
         font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))
tk.Label(hero_left, text="Your interview-prep workspace", bg=NAVY, fg=WHITE,
         font=("Segoe UI", 22, "bold")).pack(anchor="w")
tk.Label(hero_left,
         text="Save what you learn. Practise what you know. Track what to revisit.",
         bg=NAVY, fg="#DCE6FF", font=("Segoe UI", 10), wraplength=580,
         justify="left").pack(anchor="w", pady=(8, 0))
hero_actions = tk.Frame(hero, bg=NAVY)
hero_actions.grid(row=0, column=1, sticky="e", padx=(18, 0))
tk.Button(hero_actions, text="▶  Start practising", command=lambda: show_page("Practice Mode"),
          bg="#FFFFFF", fg=NAVY, activebackground="#E8EEFC", activeforeground=NAVY,
          relief="flat", bd=0, padx=17, pady=11, cursor="hand2",
          font=("Segoe UI", 10, "bold")).pack(anchor="e")
tk.Button(hero_actions, text="＋  Add interview question", command=lambda: show_page("Interview Questions"),
          bg=NAVY_LIGHT, fg=WHITE, activebackground="#304879", activeforeground=WHITE,
          relief="flat", bd=0, padx=14, pady=9, cursor="hand2",
          font=("Segoe UI", 9, "bold")).pack(anchor="e", pady=(9, 0))

# Overview heading
section_head = tk.Frame(dashboard, bg=BG)
section_head.pack(fill="x", pady=(0, 11))
tk.Label(section_head, text="YOUR LIBRARY", bg=BG, fg=TEXT,
         font=("Segoe UI", 14, "bold")).pack(side="left")
tk.Label(section_head, text="Live totals  ·  from your database", bg=BG, fg=MUTED,
         font=("Segoe UI", 9)).pack(side="right", pady=(4, 0))

# Five evenly sized cards. Cards reflow naturally into two rows on smaller screens.
stats_frame = tk.Frame(dashboard, bg=BG)
stats_frame.pack(fill="x", pady=(0, 22))
dashboard_stats = {}
stat_items = [
    ("subjects", "Subjects", "Learning areas", "#2563EB"),
    ("topics", "Topics", "Saved concepts", "#0F766E"),
    ("companies", "Companies", "Company profiles", "#7C3AED"),
    ("interviews", "Interviews", "Interview records", "#C2410C"),
    ("questions", "Questions", "Practice library", "#BE185D"),
]
for col in range(5):
    stats_frame.grid_columnconfigure(col, weight=1, uniform="stats")
for index, (stat_key, stat_title, caption, accent) in enumerate(stat_items):
    stat_card = tk.Frame(stats_frame, bg=WHITE, padx=14, pady=15,
                         highlightbackground="#E1E8F2", highlightthickness=1)
    stat_card.grid(row=0, column=index, sticky="nsew",
                   padx=(0 if index == 0 else 5, 0 if index == 4 else 5))
    tk.Frame(stat_card, bg=accent, height=4).pack(fill="x", pady=(0, 12))
    tk.Label(stat_card, text=stat_title, bg=WHITE, fg=MUTED,
             font=("Segoe UI", 9, "bold")).pack(anchor="w")
    stat_value = tk.Label(stat_card, text="—", bg=WHITE, fg=TEXT,
                          font=("Segoe UI", 25, "bold"))
    stat_value.pack(anchor="w", pady=(4, 2))
    tk.Label(stat_card, text=caption, bg=WHITE, fg=MUTED,
             font=("Segoe UI", 8)).pack(anchor="w")
    dashboard_stats[stat_key] = stat_value

# Progress section paired with a small set of helpful actions.
progress_card = tk.Frame(dashboard, bg=WHITE, padx=22, pady=19,
                         highlightbackground="#E1E8F2", highlightthickness=1)
progress_card.pack(fill="x", pady=(0, 22))
progress_top = tk.Frame(progress_card, bg=WHITE)
progress_top.pack(fill="x")
progress_title_box = tk.Frame(progress_top, bg=WHITE)
progress_title_box.pack(side="left", fill="x", expand=True)
tk.Label(progress_title_box, text="Practice progress", bg=WHITE, fg=TEXT,
         font=("Segoe UI", 14, "bold")).pack(anchor="w")
tk.Label(progress_title_box, text="Your progress is based on the status saved for each question.",
         bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))
progress_percent_label = tk.Label(progress_top, text="0%", bg=WHITE, fg=BLUE,
                                  font=("Segoe UI", 24, "bold"))
progress_percent_label.pack(side="right", padx=(12, 0))
progress_bar = tk.Canvas(progress_card, height=10, bg="#E9EEF6", highlightthickness=0, bd=0)
progress_bar.pack(fill="x", pady=(16, 11))
def draw_progress_bar(percent):
    progress_bar.delete("all")
    progress_bar.update_idletasks()
    width = max(progress_bar.winfo_width(), 1)
    progress_bar.create_rectangle(0, 0, width, 10, fill="#E9EEF6", outline="")
    if percent > 0:
        progress_bar.create_rectangle(0, 0, width * min(max(percent, 0), 100) / 100,
                                      10, fill=BLUE, outline="")
practice_progress_label = tk.Label(
    progress_card, text="Loading practice progress…", bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9), justify="left", wraplength=850
)
practice_progress_label.pack(anchor="w")
progress_actions = tk.Frame(progress_card, bg=WHITE)
progress_actions.pack(fill="x", pady=(15, 0))
tk.Button(progress_actions, text="↻  Refresh totals", command=lambda: refresh_dashboard_stats(show_errors=True),
          bg="#EEF3FC", fg=NAVY, activebackground="#DCE7F8", activeforeground=NAVY,
          relief="flat", bd=0, padx=13, pady=8, cursor="hand2",
          font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 9))
tk.Button(progress_actions, text="↓  Export backup", command=export_all_data,
          bg="#EEF3FC", fg=NAVY, activebackground="#DCE7F8", activeforeground=NAVY,
          relief="flat", bd=0, padx=13, pady=8, cursor="hand2",
          font=("Segoe UI", 9, "bold")).pack(side="left")

# Clear quick-access area: action cards are larger and grouped in two columns.
quick_header = tk.Frame(dashboard, bg=BG)
quick_header.pack(fill="x", pady=(0, 11))
tk.Label(quick_header, text="QUICK ACCESS", bg=BG, fg=TEXT,
         font=("Segoe UI", 14, "bold")).pack(side="left")
tk.Label(quick_header, text="Choose what you want to work on", bg=BG, fg=MUTED,
         font=("Segoe UI", 9)).pack(side="right", pady=(4, 0))
quick_actions = tk.Frame(dashboard, bg=BG)
quick_actions.pack(fill="x")
action_details = [
    ("Subjects", "Organise your learning areas", "01", "#2563EB"),
    ("Topics", "Review definitions and your own notes", "02", "#0F766E"),
    ("Company", "Keep track of companies and locations", "03", "#7C3AED"),
    ("Interview", "Organise roles, dates and rounds", "04", "#C2410C"),
    ("Interview Questions", "Build your question bank with answers", "05", "#BE185D"),
    ("Practice Mode", "Revise questions and update confidence", "06", "#0F766E"),
]
for index, (name, description, number, accent) in enumerate(action_details):
    row, col = divmod(index, 2)
    card = tk.Frame(quick_actions, bg=WHITE, padx=17, pady=15,
                    highlightbackground="#E1E8F2", highlightthickness=1)
    card.grid(row=row, column=col, sticky="nsew",
              padx=(0, 7) if col == 0 else (7, 0), pady=(0, 12))
    tk.Label(card, text=number, bg=accent, fg=WHITE,
             font=("Segoe UI", 9, "bold"), padx=9, pady=6).pack(side="left", padx=(0, 13))
    details = tk.Frame(card, bg=WHITE)
    details.pack(side="left", fill="x", expand=True)
    tk.Label(details, text=name, bg=WHITE, fg=TEXT,
             font=("Segoe UI", 10, "bold")).pack(anchor="w")
    tk.Label(details, text=description, bg=WHITE, fg=MUTED,
             font=("Segoe UI", 9), wraplength=310, justify="left").pack(anchor="w", pady=(4, 0))
    tk.Button(card, text="Open  ›", command=lambda n=name: show_page(n),
              bg=WHITE, fg=BLUE, activebackground="#F1F5FF", activeforeground=BLUE,
              relief="flat", bd=0, padx=8, pady=6, cursor="hand2",
              font=("Segoe UI", 9, "bold")).pack(side="right", padx=(8, 0))
quick_actions.grid_columnconfigure(0, weight=1, uniform="quick")
quick_actions.grid_columnconfigure(1, weight=1, uniform="quick")

# ---------------- CREATE DATA PAGES ----------------
for tab_name, config in TABLES.items():
    page = tk.Frame(content, bg=BG)
    pages[tab_name] = page
    # Form card
    form_card = tk.Frame(
        page,
        bg=WHITE,
        padx=22,
        pady=18,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    form_card.pack(fill="x", pady=(0, 16))
    tk.Label(
        form_card,
        text="Record details",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", pady=(0, 12))
    form_grid = tk.Frame(form_card, bg=WHITE)
    form_grid.pack(fill="x")
    widgets = {}
    for row, (field_name, label_text, field_type, required) in enumerate(
        config["fields"]
    ):
        tk.Label(
            form_grid,
            text=label_text + (" *" if required else ""),
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=row,
            column=0,
            padx=(0, 15),
            pady=7,
            sticky="w"
        )
        if field_type in ("subject", "company", "interview"):
            widget = ttk.Combobox(
                form_grid,
                width=42,
                state="readonly"
            )
        elif field_type == "text":
            widget = tk.Text(
                form_grid,
                width=45,
                height=3 if field_name == "answer" else 2,
                wrap="word",
                font=("Segoe UI", 10),
                bg="#FBFCFF",
                fg=TEXT,
                relief="solid",
                bd=1,
                padx=8,
                pady=6
            )
        else:
            widget = ttk.Entry(
                form_grid,
                width=45
            )
        widget.grid(
            row=row,
            column=1,
            padx=(0, 10),
            pady=7,
            sticky="ew"
        )
        widgets[field_name] = widget
    form_grid.columnconfigure(1, weight=1)
    # Form actions
    action_row = tk.Frame(form_card, bg=WHITE)
    action_row.pack(fill="x", pady=(15, 0))
    ttk.Button(
        action_row,
        text="Save Record",
        style="Primary.TButton",
        command=lambda n=tab_name: save_record(n)
    ).pack(side="left", padx=(0, 8))
    ttk.Button(
        action_row,
        text="Clear Fields",
        style="Secondary.TButton",
        command=lambda n=tab_name: clear_form(n)
    ).pack(side="left", padx=(0, 8))
    ttk.Button(
        action_row,
        text="Refresh Records",
        style="Secondary.TButton",
        command=lambda n=tab_name: refresh_records(n)
    ).pack(side="left")
    # Records card
    records_card = tk.Frame(
        page,
        bg=WHITE,
        padx=14,
        pady=12,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    records_card.pack(fill="both", expand=True)
    records_header = tk.Frame(records_card, bg=WHITE)
    records_header.pack(fill="x", pady=(0, 10))
    tk.Label(
        records_header,
        text="Saved records",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 13, "bold")
    ).pack(side="left")
    record_count = tk.Label(
        records_header,
        text="0 records",
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9)
    )
    record_count.pack(side="right", padx=(12, 0))
    tk.Label(
        records_header,
        text="Data from MySQL",
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(side="right")
    # Search controls for records saved in this section.
    search_row = tk.Frame(records_card, bg=WHITE)
    search_row.pack(fill="x", pady=(0, 10))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_row, textvariable=search_var, width=38)
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
    search_entry.bind("<Return>", lambda event, n=tab_name: refresh_records(n))
    ttk.Button(
        search_row,
        text="Search",
        style="Primary.TButton",
        command=lambda n=tab_name: refresh_records(n)
    ).pack(side="left", padx=(0, 8))
    ttk.Button(
        search_row,
        text="Clear Search",
        style="Secondary.TButton",
        command=lambda n=tab_name: clear_search(n)
    ).pack(side="left", padx=(0, 8))
    ttk.Button(
        search_row,
        text="View Full Details",
        style="Secondary.TButton",
        command=lambda n=tab_name: show_record_details(n)
    ).pack(side="left")
    table_frame = tk.Frame(records_card, bg=WHITE)
    table_frame.pack(fill="both", expand=True)
    tree = ttk.Treeview(
        table_frame,
        columns=config["columns"],
        show="headings"
    )
    tree.bind("<Double-1>", lambda event, n=tab_name: show_record_details(n))
    # Give text-heavy columns more room so table values do not look crowded.
    column_widths = {
        "sub_id": 85,
        "sub_name": 180,
        "topic_id": 85,
        "topic_name": 200,
        "computer_definationa": 320,
        "my_defination": 320,
        "comp_id": 85,
        "comp_name": 210,
        "location": 180,
        "interview_id": 100,
        "job_role": 200,
        "inteview_date": 150,
        "rounds": 90,
        "comp_id": 100,
        "question_no": 100,
        "question": 380,
        "question_type": 170,
        "answer": 380,
        "practice_status": 150,
        "confidence_level": 140,
        "last_practiced": 140,
    }
    for column in config["columns"]:
        tree.heading(
            column,
            text=column.replace("_", " ").title(),
            command=lambda c=column, n=tab_name: sort_table(n, c)
        )
        tree.column(
            column,
            width=column_widths.get(column, 170),
            minwidth=85,
            anchor="w",
            stretch=False
        )
    y_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )
    x_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )
    tree.configure(
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
    tree.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")
    x_scroll.grid(row=1, column=0, sticky="ew")
    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)
    forms[tab_name] = {
        "widgets": widgets,
        "tree": tree,
        "search_var": search_var,
        "record_count": record_count
    }
# ---------------- INTERVIEW PRACTICE MODE ----------------
practice_page = tk.Frame(content, bg=BG)
pages["Practice Mode"] = practice_page

# Practice Mode is taller than a typical window. Put its controls inside a
# vertically scrollable canvas so the answer editor and action buttons remain
# reachable on smaller screens.
practice_canvas = tk.Canvas(
    practice_page, bg=BG, highlightthickness=0, borderwidth=0
)
practice_scrollbar = ttk.Scrollbar(
    practice_page, orient="vertical", command=practice_canvas.yview
)
practice_canvas.configure(yscrollcommand=practice_scrollbar.set)
practice_scrollbar.pack(side="right", fill="y")
practice_canvas.pack(side="left", fill="both", expand=True)
practice_body = tk.Frame(practice_canvas, bg=BG)
practice_body_window = practice_canvas.create_window(
    (0, 0), window=practice_body, anchor="nw"
)

def _update_practice_scroll_region(_event=None):
    practice_canvas.configure(scrollregion=practice_canvas.bbox("all"))

def _fit_practice_body_width(event):
    practice_canvas.itemconfigure(practice_body_window, width=event.width)

# Keep one application-wide mouse-wheel handler. A bind_all handler alone
# can be blocked by Tkinter Text/Combobox class bindings, so give every widget
# inside the scrollable pages a custom bindtag that runs before widget classes.
def _app_mousewheel(event):
    if current_page == "Practice Mode":
        target_canvas = practice_canvas
    elif current_page == "Dashboard":
        target_canvas = dashboard_canvas
    else:
        return None

    if getattr(event, "num", None) == 4:       # Linux: wheel up
        direction, units = -1, 3
    elif getattr(event, "num", None) == 5:     # Linux: wheel down
        direction, units = 1, 3
    else:                                      # Windows / macOS
        delta = getattr(event, "delta", 0)
        if not delta:
            return "break"
        direction = -1 if delta > 0 else 1
        # Windows uses multiples of 120; trackpads may send smaller deltas.
        units = max(1, min(5, round(abs(delta) / 120)))

    target_canvas.yview_scroll(direction * units, "units")
    return "break"

_MOUSEWHEEL_TAG = "MyMemoryMouseWheel"

def _install_mousewheel_tag(widget):
    try:
        tags = list(widget.bindtags())
        if _MOUSEWHEEL_TAG not in tags:
            tags.insert(0, _MOUSEWHEEL_TAG)
            widget.bindtags(tuple(tags))
    except tk.TclError:
        pass
    for child in widget.winfo_children():
        _install_mousewheel_tag(child)

# This tag runs before Text/Combobox class bindings, which can consume wheel events.
root.bind_class(_MOUSEWHEEL_TAG, "<MouseWheel>", _app_mousewheel)
root.bind_class(_MOUSEWHEEL_TAG, "<Button-4>", _app_mousewheel)
root.bind_class(_MOUSEWHEEL_TAG, "<Button-5>", _app_mousewheel)

practice_body.bind("<Configure>", _update_practice_scroll_region)
practice_canvas.bind("<Configure>", _fit_practice_body_width)
# add='+' preserves any other Tk bindings; this is the only global wheel route.
root.bind_all("<MouseWheel>", _app_mousewheel, add="+")
root.bind_all("<Button-4>", _app_mousewheel, add="+")
root.bind_all("<Button-5>", _app_mousewheel, add="+")

practice_questions = []
practice_index = 0
practice_results = {}
practice_drafts = {}
practice_details_visible = False

practice_intro = tk.Frame(
    practice_body, bg=WHITE, padx=22, pady=18,
    highlightbackground="#E2E8F0", highlightthickness=1
)
practice_intro.pack(fill="x", pady=(0, 14))
tk.Label(
    practice_intro, text="Interview Practice Mode", bg=WHITE, fg=NAVY,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w")
tk.Label(
    practice_intro,
    text="Answer each saved question aloud or in the box below, then check the interview details and mark your result.",
    bg=WHITE, fg=MUTED, font=("Segoe UI", 10), wraplength=850, justify="left"
).pack(anchor="w", pady=(6, 12))
practice_top_row = tk.Frame(practice_intro, bg=WHITE)
practice_top_row.pack(fill="x")
practice_counter = tk.Label(
    practice_top_row, text="No questions loaded", bg=WHITE, fg=BLUE,
    font=("Segoe UI", 10, "bold")
)
practice_counter.pack(side="left")
practice_status = tk.Label(
    practice_top_row, text="", bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9)
)
practice_status.pack(side="right")

confidence_row = tk.Frame(practice_intro, bg=WHITE)
confidence_row.pack(fill="x", pady=(10, 0))
tk.Label(
    confidence_row, text="Confidence (0–5):", bg=WHITE, fg=TEXT,
    font=("Segoe UI", 9, "bold")
).pack(side="left", padx=(0, 8))
confidence_var = tk.StringVar(value="0")
confidence_picker = ttk.Combobox(
    confidence_row, textvariable=confidence_var, values=("0", "1", "2", "3", "4", "5"),
    width=5, state="readonly"
)
confidence_picker.pack(side="left")
ttk.Button(
    confidence_row, text="Save Confidence", style="Secondary.TButton",
    command=lambda: save_practice_confidence()
).pack(side="left", padx=8)

question_select_row = tk.Frame(practice_intro, bg=WHITE)
question_select_row.pack(fill="x", pady=(12, 0))
tk.Label(
    question_select_row, text="Choose a question:", bg=WHITE, fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(side="left", padx=(0, 10))
question_choice_var = tk.StringVar(value="")
question_selector = ttk.Combobox(
    question_select_row, textvariable=question_choice_var,
    state="readonly", width=80
)
question_selector.pack(side="left", fill="x", expand=True)
question_selector.bind("<<ComboboxSelected>>", lambda _event: None)

practice_card = tk.Frame(
    practice_body, bg=WHITE, padx=22, pady=20,
    highlightbackground="#E2E8F0", highlightthickness=1
)
practice_card.pack(fill="both", expand=True)
tk.Label(
    practice_card, text="QUESTION", bg=WHITE, fg=MUTED,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w")
question_display = tk.Text(
    practice_card, height=4, wrap="word", font=("Segoe UI", 15, "bold"),
    bg="#F5F8FF", fg=NAVY, relief="flat", padx=16, pady=14
)
question_display.pack(fill="x", pady=(8, 16))
question_display.configure(state="disabled")
tk.Label(
    practice_card, text="YOUR ANSWER", bg=WHITE, fg=NAVY,
    font=("Segoe UI", 10, "bold")
).pack(anchor="w")
answer_box = tk.Text(
    practice_card, height=6, wrap="word", font=("Segoe UI", 10),
    bg="#FBFCFF", fg=TEXT, relief="solid", bd=1,
    padx=12, pady=10
)
answer_box.pack(fill="both", expand=True, pady=(7, 12))
tk.Label(
    practice_card,
    text="Type your own answer here. Click Check Progress to compare it with the saved expected answer.",
    bg=WHITE, fg=MUTED, font=("Segoe UI", 9), wraplength=850, justify="left"
).pack(anchor="w", pady=(0, 8))
progress_row = tk.Frame(practice_card, bg=WHITE)
progress_row.pack(fill="x", pady=(0, 12))
ttk.Button(
    progress_row, text="Check Progress", style="Primary.TButton",
    command=lambda: check_answer_progress()
).pack(side="left")
progress_result = tk.Label(
    progress_row, text="", bg=WHITE, fg=BLUE,
    font=("Segoe UI", 10, "bold"), wraplength=700, justify="left"
)
progress_result.pack(side="left", padx=12, fill="x", expand=True)

tk.Label(
    practice_card, text="SAVED EXPECTED ANSWER (stored in MySQL)", bg=WHITE,
    fg=NAVY, font=("Segoe UI", 10, "bold")
).pack(anchor="w")
saved_answer_box = tk.Text(
    practice_card, height=4, wrap="word", font=("Segoe UI", 10),
    bg="#F8FAFF", fg=TEXT, relief="solid", bd=1, padx=12, pady=10
)
saved_answer_box.pack(fill="x", pady=(7, 8))
saved_answer_box.insert("1.0", "Answer hidden. Click Reveal Expected Answer when you are ready.")
saved_answer_box.configure(state="disabled")
expected_answer_buttons = tk.Frame(practice_card, bg=WHITE)
expected_answer_buttons.pack(fill="x", pady=(0, 12))
ttk.Button(
    expected_answer_buttons, text="Reveal Expected Answer", style="Secondary.TButton",
    command=lambda: reveal_expected_answer()
).pack(side="left", padx=(0, 8))
ttk.Button(
    expected_answer_buttons, text="Edit Expected Answer", style="Secondary.TButton",
    command=lambda: edit_expected_answer()
).pack(side="left", padx=(0, 8))
ttk.Button(
    expected_answer_buttons, text="Save Expected Answer", style="Primary.TButton",
    command=lambda: save_expected_answer()
).pack(side="left")

revealed_details = tk.Text(
    practice_card, height=5, wrap="word", font=("Segoe UI", 10),
    bg="#F1F5F9", fg=TEXT, relief="flat", padx=12, pady=10
)
revealed_details.pack(fill="x", pady=(0, 12))
revealed_details.insert("1.0", "Saved interview details will appear here when you choose Reveal Saved Details.")
revealed_details.configure(state="disabled")

practice_button_row = tk.Frame(practice_card, bg=WHITE)
practice_button_row.pack(fill="x", pady=(2, 0))
practice_prev_button = ttk.Button(
    practice_button_row, text="← Previous", style="Secondary.TButton",
    command=lambda: move_practice(-1)
)
practice_prev_button.pack(side="left", padx=(0, 8))
practice_next_button = ttk.Button(
    practice_button_row, text="Next →", style="Primary.TButton",
    command=lambda: move_practice(1)
)
practice_next_button.pack(side="left", padx=(0, 8))
practice_reveal_button = ttk.Button(
    practice_button_row, text="Reveal Saved Details", style="Secondary.TButton",
    command=lambda: reveal_practice_details()
)
practice_reveal_button.pack(side="left", padx=(0, 8))
practice_got_button = ttk.Button(
    practice_button_row, text="✓ Got It", style="Secondary.TButton",
    command=lambda: mark_practice_result("Got it")
)
practice_got_button.pack(side="right", padx=(8, 0))
practice_revision_button = ttk.Button(
    practice_button_row, text="↻ Need Revision", style="Secondary.TButton",
    command=lambda: mark_practice_result("Need revision")
)
practice_revision_button.pack(side="right")


def set_practice_text(widget, value):
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", value)
    widget.configure(state="disabled")


def load_practice_questions():
    global practice_questions, practice_index, practice_details_visible
    previously_selected_id = None
    if practice_questions and 0 <= practice_index < len(practice_questions):
        save_current_practice_draft()
        previously_selected_id = practice_questions[practice_index][0]
    try:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "SELECT q.question_no, q.question, q.question_type, q.answer, "
                    "q.practice_status, q.confidence_level, q.last_practiced, "
                    "i.job_role, i.inteview_date, i.rounds, c.comp_name "
                    "FROM inter_questions q "
                    "LEFT JOIN interview i ON q.interview_id = i.interview_id "
                    "LEFT JOIN company c ON i.comp_id = c.comp_id "
                    "WHERE q.question IS NOT NULL AND TRIM(q.question) <> '' "
                    "ORDER BY q.question_no"
                )
                practice_questions = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            connection.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Practice Mode Error", str(error), parent=root)
        return

    selector_options = [
        f"Q{row[0]}: {str(row[1] or '').strip().replace(chr(10), ' ')[:115]}"
        for row in practice_questions
    ]
    question_selector.configure(values=selector_options)
    if practice_questions:
        matching_index = next(
            (i for i, row in enumerate(practice_questions) if row[0] == previously_selected_id),
            None
        )
        if matching_index is not None:
            practice_index = matching_index
        else:
            practice_index = min(practice_index, len(practice_questions) - 1)
    else:
        practice_index = 0
    practice_details_visible = False
    if not practice_questions:
        question_choice_var.set("")
        progress_result.config(text="")
    if not practice_questions:
        practice_counter.config(text="0 questions")
        practice_status.config(text="Add questions in Interview Questions first.")
        set_practice_text(
            question_display,
            "No valid interview questions found. Add a question with actual text in the Interview Questions page. "
            "Rows that only have a question number are old empty records and are not shown here."
        )
        answer_box.delete("1.0", "end")
        saved_answer_box.configure(state="normal")
        saved_answer_box.delete("1.0", "end")
        saved_answer_box.insert("1.0", "No saved answer available.")
        saved_answer_box.configure(state="disabled")
        set_practice_text(revealed_details, "No saved interview details available.")
        return
    show_practice_question()


def show_practice_question():
    global practice_details_visible
    if not practice_questions:
        return
    question = practice_questions[practice_index]
    question_no = question[0]
    question_text = str(question[1] or "").strip()
    if question_selector['values'] and practice_index < len(question_selector['values']):
        question_choice_var.set(question_selector['values'][practice_index])
    progress_result.config(text="")
    set_practice_text(
        question_display,
        f"Question ID: {question_no}\n\n{question_text if question_text else '⚠ This record has no question text. Edit it in Interview Questions.'}"
    )
    answer_box.delete("1.0", "end")
    answer_box.insert("1.0", practice_drafts.get(question_no, ""))
    saved_answer_box.configure(state="normal")
    saved_answer_box.delete("1.0", "end")
    saved_answer_box.insert("1.0", "Answer hidden. Click Reveal Expected Answer when you are ready.")
    saved_answer_box.configure(state="disabled")
    practice_counter.config(
        text=f"Question {practice_index + 1} of {len(practice_questions)}"
    )
    result = question[4] or "Not Started"
    practice_results[question_no] = result
    practice_status.config(text=f"Result: {result}")
    confidence_var.set(str(question[5] if question[5] is not None else 0))
    practice_prev_button.configure(state="normal" if practice_index > 0 else "disabled")
    practice_next_button.configure(
        state="normal" if practice_index < len(practice_questions) - 1 else "disabled"
    )
    practice_details_visible = False
    set_practice_text(
        revealed_details,
        "Saved interview details will appear here when you choose Reveal Saved Details."
    )


def on_question_selected(_event=None):
    global practice_index
    if not practice_questions:
        return
    selected = question_choice_var.get()
    values = list(question_selector.cget("values"))
    try:
        practice_index = values.index(selected)
    except ValueError:
        return
    show_practice_question()


def check_answer_progress():
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    question = practice_questions[practice_index]
    expected = str(question[3] or "").strip()
    user_answer = answer_box.get("1.0", "end-1c").strip()
    if not user_answer:
        messagebox.showwarning("Answer Required", "Write your answer first, then check progress.", parent=root)
        return
    if not expected:
        messagebox.showwarning(
            "Expected Answer Missing",
            "There is no saved expected answer for this question yet. Add one using Edit Expected Answer, then Save Expected Answer.",
            parent=root
        )
        return

    # Text similarity is a rough wording comparison, not an AI judgement of correctness.
    user_norm = re.sub(r"\s+", " ", user_answer.lower()).strip()
    expected_norm = re.sub(r"\s+", " ", expected.lower()).strip()
    sequence_score = SequenceMatcher(None, user_norm, expected_norm).ratio()
    user_words = set(re.findall(r"\b[\w]+\b", user_norm))
    expected_words = set(re.findall(r"\b[\w]+\b", expected_norm))
    word_score = len(user_words & expected_words) / max(1, len(expected_words))
    similarity = round(((sequence_score * 0.4) + (word_score * 0.6)) * 100)
    # Highlight a few expected-answer terms the learner may want to revisit.
    stop_words = {"the", "and", "for", "with", "that", "this", "are", "was", "from", "into", "have", "has", "use", "used", "using", "you", "your", "its", "their", "can", "will", "not", "but", "when", "what", "how", "then", "than", "also", "such", "one", "each", "all"}
    important_terms = {word for word in expected_words if len(word) >= 4 and word not in stop_words}
    missing_terms = sorted(important_terms - user_words)
    practice_drafts[question[0]] = user_answer
    saved_answer_box.configure(state="normal")
    saved_answer_box.delete("1.0", "end")
    saved_answer_box.insert("1.0", expected)
    saved_answer_box.configure(state="disabled")
    if similarity >= 75:
        feedback = "Good wording match — still verify the key concepts."
    elif similarity >= 45:
        feedback = "Partial wording match — compare your answer with the expected answer below."
    else:
        feedback = "Low wording match — review the expected answer below."
    missing_text = ("Possible key terms to revisit: " + ", ".join(missing_terms[:8])) if missing_terms else "No obvious key terms missing from the expected answer."
    progress_result.config(
        text=f"Text similarity: {similarity}%  |  {feedback}\n{missing_text}\nNote: this is a wording aid, not a correctness score."
    )


question_selector.bind("<<ComboboxSelected>>", on_question_selected)


def save_current_practice_draft():
    if not practice_questions or not (0 <= practice_index < len(practice_questions)):
        return
    question_no = practice_questions[practice_index][0]
    practice_drafts[question_no] = answer_box.get("1.0", "end-1c")


def move_practice(direction):
    global practice_index
    if not practice_questions:
        return
    save_current_practice_draft()
    next_index = practice_index + direction
    if 0 <= next_index < len(practice_questions):
        practice_index = next_index
        show_practice_question()


def reveal_practice_details():
    global practice_details_visible
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    save_current_practice_draft()
    question = practice_questions[practice_index]
    question_no, question_text, question_type, saved_answer, saved_status, confidence, last_practiced, job_role, interview_date, rounds, company_name = question
    details = (
        f"Question type: {question_type or 'Not specified'}\n"
        f"Company: {company_name or 'Not specified'}\n"
        f"Job role: {job_role or 'Not specified'}\n"
        f"Interview date: {interview_date or 'Not specified'}\n"
        f"Number of rounds: {rounds if rounds is not None else 'Not specified'}\n"
        f"Practice status: {saved_status or 'Not Started'}\n"
        f"Confidence: {confidence if confidence is not None else 0}/5\n"
        f"Last practiced: {last_practiced or 'Never'}"
    )
    set_practice_text(revealed_details, details)
    practice_details_visible = True


def reveal_expected_answer():
    """Reveal the stored answer only after the learner requests it."""
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    question = practice_questions[practice_index]
    answer = str(question[3] or "").strip()
    saved_answer_box.configure(state="normal")
    saved_answer_box.delete("1.0", "end")
    saved_answer_box.insert("1.0", answer if answer else "No expected answer has been saved for this question yet.")
    saved_answer_box.configure(state="disabled")


def edit_expected_answer():
    """Load the current stored answer into the editor for updating."""
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    question = practice_questions[practice_index]
    saved_answer_box.configure(state="normal")
    saved_answer_box.delete("1.0", "end")
    saved_answer_box.insert("1.0", str(question[3] or ""))
    saved_answer_box.focus_set()


def save_expected_answer():
    global practice_index
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    if str(saved_answer_box.cget("state")) != "normal":
        messagebox.showinfo(
            "Edit Expected Answer First",
            "Click 'Edit Expected Answer' before saving changes.",
            parent=root
        )
        return
    question_no = practice_questions[practice_index][0]
    saved_answer = saved_answer_box.get("1.0", "end-1c").strip()
    try:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE inter_questions SET answer = %s WHERE question_no = %s",
                    (saved_answer or None, question_no)
                )
                connection.commit()
            finally:
                cursor.close()
        finally:
            connection.close()
        current_index = practice_index
        load_practice_questions()
        if practice_questions:
            practice_index = min(current_index, len(practice_questions) - 1)
            show_practice_question()
        messagebox.showinfo("Answer Saved", "Expected answer saved to MySQL.", parent=root)
    except mysql.connector.Error as error:
        messagebox.showerror("Could Not Save Expected Answer", str(error), parent=root)


def save_practice_confidence():
    global practice_index
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    try:
        confidence = int(confidence_var.get())
        if confidence < 0 or confidence > 5:
            raise ValueError
        question_no = practice_questions[practice_index][0]
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE inter_questions SET confidence_level = %s WHERE question_no = %s",
                    (confidence, question_no)
                )
                connection.commit()
            finally:
                cursor.close()
        finally:
            connection.close()
        current_index = practice_index
        load_practice_questions()
        practice_index = min(current_index, len(practice_questions) - 1) if practice_questions else 0
        if practice_questions:
            show_practice_question()
        messagebox.showinfo("Saved", "Confidence level saved.", parent=root)
    except ValueError:
        messagebox.showwarning("Invalid Confidence", "Choose a confidence level from 0 to 5.", parent=root)
    except mysql.connector.Error as error:
        messagebox.showerror("Could Not Save Confidence", str(error), parent=root)


def mark_practice_result(result):
    global practice_index
    if not practice_questions:
        messagebox.showinfo("No Questions", "Load some interview questions first.", parent=root)
        return
    save_current_practice_draft()
    question_no = practice_questions[practice_index][0]
    try:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "UPDATE inter_questions "
                    "SET practice_status = %s, last_practiced = %s "
                    "WHERE question_no = %s",
                    (result, date.today(), question_no)
                )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()
        finally:
            connection.close()
        practice_results[question_no] = result
        practice_status.config(text=f"Result: {result}")
        current_index = practice_index
        load_practice_questions()
        if practice_questions:
            practice_index = min(current_index, len(practice_questions) - 1)
            show_practice_question()
        refresh_dashboard_stats(show_errors=False)
        messagebox.showinfo("Practice Saved", f"Question marked '{result}' and saved.", parent=root)
    except mysql.connector.Error as error:
        messagebox.showerror("Could Not Save Practice Result", str(error), parent=root)


practice_load_row = tk.Frame(practice_body, bg=BG)
practice_load_row.pack(fill="x", pady=(12, 0))
ttk.Button(
    practice_load_row, text="Load / Refresh Questions", style="Primary.TButton",
    command=load_practice_questions
).pack(side="left")
tk.Label(
    practice_load_row,
    text="Practice status, confidence, and last-practiced date are saved to MySQL.",
    bg=BG, fg=MUTED, font=("Segoe UI", 9), wraplength=650, justify="left"
).pack(side="left", padx=12)

# Ensure mouse-wheel scrolling works over every Practice Mode control. Tk's
# widget/class bindings can consume wheel events before bind_all sees them, so
# put a dedicated bindtag FIRST in each widget's bindtag list.
_PRACTICE_WHEEL_TAG = "PracticeModeMouseWheel"

def _practice_wheel_event(event):
    if current_page != "Practice Mode":
        return None
    if getattr(event, "num", None) == 4:       # Linux wheel up
        direction = -1
        units = 3
    elif getattr(event, "num", None) == 5:     # Linux wheel down
        direction = 1
        units = 3
    else:                                      # Windows / macOS
        delta = getattr(event, "delta", 0)
        if not delta:
            return "break"
        direction = -1 if delta > 0 else 1
        # Windows commonly reports +/-120; trackpads may report smaller steps.
        units = max(1, min(5, round(abs(delta) / 120)))
    practice_canvas.yview_scroll(direction * units, "units")
    return "break"

root.bind_class(_PRACTICE_WHEEL_TAG, "<MouseWheel>", _practice_wheel_event)
root.bind_class(_PRACTICE_WHEEL_TAG, "<Button-4>", _practice_wheel_event)
root.bind_class(_PRACTICE_WHEEL_TAG, "<Button-5>", _practice_wheel_event)

def _bind_practice_wheel(widget):
    tags = list(widget.bindtags())
    if _PRACTICE_WHEEL_TAG not in tags:
        widget.bindtags((_PRACTICE_WHEEL_TAG, *tags))
    for child in widget.winfo_children():
        _bind_practice_wheel(child)

_bind_practice_wheel(practice_body)
practice_canvas.after_idle(_update_practice_scroll_region)

# ---------------- SIDEBAR NAV ITEMS ----------------
create_nav_button("Dashboard", "⌂")
for name, symbol in [
    ("Subjects", "S"),
    ("Topics", "T"),
    ("Company", "C"),
    ("Interview", "I"),
    ("Interview Questions", "Q"),
    ("Practice Mode", "P")
]:
    create_nav_button(name, symbol)
tk.Frame(sidebar, bg=NAVY).pack(fill="both", expand=True)
tk.Label(
    sidebar,
    text="MY MEMORY  •  PYTHON",
    bg=NAVY,
    fg="#91A6D0",
    font=("Segoe UI", 8)
).pack(anchor="w", padx=20, pady=20)
# ---------------- START ----------------
show_page("Dashboard")
try:
    refresh_all()
except mysql.connector.Error as error:
    messagebox.showerror(
        "Database Connection Error",
        str(error)
    )
def _install_scroll_tags_for_pages():
    _install_mousewheel_tag(practice_page)
    _install_mousewheel_tag(dashboard_shell)

root.after_idle(_install_scroll_tags_for_pages)

root.mainloop()
