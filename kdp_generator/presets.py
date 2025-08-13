import os
from typing import List, Tuple

from .notebook import render_notebook_pdf
from .notebooks_extra import (
    render_daily_planner_pdf,
    render_monthly_planner_pdf,
    render_habit_tracker_pdf,
    render_budget_planner_pdf,
    render_recipe_book_pdf,
    render_grid_notebook_pdf,
    render_bullet_journal_pdf,
)
from .paper import render_graph_paper_pdf, render_isometric_paper_pdf, render_music_staff_paper_pdf
from .education import render_tracing_letters_pdf

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "outputs"))


def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def presets() -> List[Tuple[str, callable]]:
    title_only = [
        ("gratitude_journal.pdf", lambda: render_notebook_pdf("Gratitude Journal", 120, "lined", os.path.join(OUTPUT_DIR, "gratitude_journal.pdf"), "6x9")),
        ("travel_journal.pdf", lambda: render_notebook_pdf("Travel Journal", 120, "dotted", os.path.join(OUTPUT_DIR, "travel_journal.pdf"), "6x9")),
        ("fitness_logbook.pdf", lambda: render_notebook_pdf("Fitness Logbook", 120, "lined", os.path.join(OUTPUT_DIR, "fitness_logbook.pdf"), "6x9")),
        ("meal_planner.pdf", lambda: render_notebook_pdf("Meal Planner", 120, "lined", os.path.join(OUTPUT_DIR, "meal_planner.pdf"), "6x9")),
        ("baby_logbook.pdf", lambda: render_notebook_pdf("Baby Logbook", 120, "lined", os.path.join(OUTPUT_DIR, "baby_logbook.pdf"), "6x9")),
        ("pregnancy_journal.pdf", lambda: render_notebook_pdf("Pregnancy Journal", 120, "dotted", os.path.join(OUTPUT_DIR, "pregnancy_journal.pdf"), "6x9")),
        ("reading_log.pdf", lambda: render_notebook_pdf("Reading Log", 120, "lined", os.path.join(OUTPUT_DIR, "reading_log.pdf"), "6x9")),
        ("music_practice_log.pdf", lambda: render_notebook_pdf("Music Practice Log", 120, "lined", os.path.join(OUTPUT_DIR, "music_practice_log.pdf"), "6x9")),
        ("language_study_notebook.pdf", lambda: render_notebook_pdf("Language Study Notebook", 120, "dotted", os.path.join(OUTPUT_DIR, "language_study_notebook.pdf"), "6x9")),
        ("project_planner.pdf", lambda: render_notebook_pdf("Project Planner", 120, "dotted", os.path.join(OUTPUT_DIR, "project_planner.pdf"), "6x9")),
        ("startup_idea_log.pdf", lambda: render_notebook_pdf("Startup Idea Log", 120, "dotted", os.path.join(OUTPUT_DIR, "startup_idea_log.pdf"), "6x9")),
        ("sketchbook_85x11.pdf", lambda: render_notebook_pdf("Sketchbook", 120, "blank", os.path.join(OUTPUT_DIR, "sketchbook_85x11.pdf"), "8.5x11")),
        ("dot_grid_notebook.pdf", lambda: render_bullet_journal_pdf("Dot Grid Notebook", 120, os.path.join(OUTPUT_DIR, "dot_grid_notebook.pdf"), "6x9", spacing=18.0)),
        ("teacher_planner.pdf", lambda: render_monthly_planner_pdf(12, os.path.join(OUTPUT_DIR, "teacher_planner.pdf"), "8.5x11")),
        ("wedding_planner.pdf", lambda: render_monthly_planner_pdf(12, os.path.join(OUTPUT_DIR, "wedding_planner.pdf"), "8.5x11")),
        ("budget_binder.pdf", lambda: render_budget_planner_pdf(12, os.path.join(OUTPUT_DIR, "budget_binder.pdf"), "8.5x11")),
        ("gratitude_5min.pdf", lambda: render_daily_planner_pdf(60, os.path.join(OUTPUT_DIR, "gratitude_5min.pdf"), "6x9")),
        ("goal_planner.pdf", lambda: render_daily_planner_pdf(90, os.path.join(OUTPUT_DIR, "goal_planner.pdf"), "8.5x11")),
        ("lesson_planner.pdf", lambda: render_daily_planner_pdf(60, os.path.join(OUTPUT_DIR, "lesson_planner.pdf"), "8.5x11")),
        ("music_staff_paper.pdf", lambda: render_music_staff_paper_pdf(os.path.join(OUTPUT_DIR, "music_staff_paper.pdf"), 8, "8.5x11")),
        ("graph_paper_025.pdf", lambda: render_graph_paper_pdf(os.path.join(OUTPUT_DIR, "graph_paper_025.pdf"), 0.25, "8.5x11")),
        ("isometric_paper_025.pdf", lambda: render_isometric_paper_pdf(os.path.join(OUTPUT_DIR, "isometric_paper_025.pdf"), 0.25, "8.5x11")),
        ("calligraphy_practice.pdf", lambda: render_tracing_letters_pdf(os.path.join(OUTPUT_DIR, "calligraphy_practice.pdf"), pages=10, text="ABCDEFGHIJKLMNOPQRSTUVWXYZ", trim_size="8.5x11")),
    ]

    more_titles = [
        "Gratitude Journal Midnight", "Daily Wellness Journal", "Mindfulness Journal", "Dream Journal", "Prayer Journal",
        "Budget Planner Classic", "Bill Tracker", "Expense Tracker", "Password Logbook", "Address Book",
        "Recipe Journal", "Baking Journal", "Wine Tasting Journal", "Coffee Tasting Journal", "Travel Planner",
        "Hiking Logbook", "Camping Logbook", "Fishing Logbook", "RV Travel Journal", "Car Maintenance Log",
        "Pet Care Log", "Cat Health Record", "Dog Health Record", "Baby Feeding Log", "Baby Sleep Log",
        "Workout Log", "Running Log", "Cycling Log", "Yoga Journal", "Pilates Journal",
        "Teacher Grade Book", "Student Planner", "Homework Planner", "Study Planner", "Language Vocabulary Log",
        "Reading Tracker", "Book Review Journal", "Movie Review Journal", "Gardening Journal", "House Cleaning Planner",
        "Meal Plan & Grocery List", "Intermittent Fasting Tracker", "Water Tracker", "Habit Journal", "Morning Routine Planner",
        "Evening Routine Planner", "Self-Care Planner", "Anxiety Journal", "Mood Tracker", "Sermon Notes",
        # add many more to surpass 100
        "Dental Care Log", "Medical Appointment Log", "Blood Pressure Log", "Glucose Tracker", "Symptom Tracker",
        "Medication Log", "Allergy Journal", "Pain Tracker", "Physio Exercise Log", "Rehab Journal",
        "Budget Monthly Planner", "Debt Snowball Tracker", "Savings Tracker", "Investment Journal", "Expense Category Ledger",
        "Content Planner", "Social Media Planner", "YouTube Planning", "Podcast Planner", "Blog Planner",
        "Etsy Product Planner", "Amazon Seller Planner", "Shop Inventory Log", "Order Tracker", "Shipping Log",
        "Class Notes", "Lecture Notes", "Lab Notebook", "Research Journal", "Citation Log",
        "Vacation Planner", "City Trip Planner", "Packing Checklist", "Itinerary Planner", "Travel Expenses Log",
        "Wedding Guest List", "Wedding Vendor List", "Wedding Budget", "Seating Chart Notes", "Venue Planning",
        "Chore Chart", "Weekly Chore Planner", "Home Maintenance Log", "Yard Work Planner", "Plant Watering Log",
        "Greenhouse Journal", "Seed Starting Log", "Herb Garden Journal", "Vegetable Garden Planner", "Flower Garden Planner",
        "Music Composition Book", "Guitar Practice Log", "Piano Practice Log", "Singing Practice Log", "Band Rehearsal Notes",
        "Art Sketch Journal", "Watercolor Journal", "Comics Planning", "Storyboard Notebook", "Photography Shot List",
        "Coding Journal", "Bug Hunting Log", "Feature Ideas Log", "System Design Notes", "Interview Prep Notebook",
        "Reading Challenge Tracker", "Book Series Tracker", "Library Loans Log", "Wish List Planner", "Gift Planner",
        "Mind Map Notebook", "Brain Dump Journal", "Ideas Capture", "Daily Prompts Journal", "Quotes Collection",
        "Language Grammar Notes", "Kanji Practice Book", "Vocabulary Builder", "Conversation Phrases", "Pronunciation Practice",
    ]

    for name in more_titles:
        slug = name.lower().replace(" ", "_").replace("&", "and").replace("/", "-")
        path = os.path.join(OUTPUT_DIR, f"{slug}.pdf")
        style = "lined"
        if any(k in name.lower() for k in ["dot", "grid", "bullet", "planner", "journal", "notes", "log", "tracker"]):
            style = "dotted"
        if any(k in name.lower() for k in ["sketch", "draw", "art", "watercolor"]):
            style = "blank"
        title_only.append((f"{slug}.pdf", lambda n=name, s=style, p=path: render_notebook_pdf(n, 120, s, p, "6x9")))

    return title_only


def main():
    ensure_dir()
    for out_name, fn in presets():
        try:
            fn()
            print("Generated:", out_name)
        except Exception as e:
            print("Failed:", out_name, e)


if __name__ == "__main__":
    main()