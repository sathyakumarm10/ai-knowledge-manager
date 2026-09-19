import json
import os
from datetime import datetime


DATA_FILE = "notes.json"


def load_notes():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_notes():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4, ensure_ascii=False)


notes = load_notes()


def get_next_id():
    if not notes:
        return 1

    existing_ids = []

    for note in notes:
        if "id" in note:
            existing_ids.append(note["id"])

    if not existing_ids:
        return 1

    return max(existing_ids) + 1


def show_menu():
    print("\n================================")
    print("       KNOWLEDGE MANAGER")
    print("================================")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Search Notes")
    print("4. View Notes by Topic")
    print("5. Search by Tag")
    print("6. Delete Note")
    print("7. Exit")


def add_note():
    title = input("Enter note title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    topic = input("Enter topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    tags_input = input(
        "Enter tags separated by commas: "
    ).strip()

    tags = []

    if tags_input:
        for tag in tags_input.split(","):
            cleaned_tag = tag.strip().lower()

            if cleaned_tag:
                tags.append(cleaned_tag)

    content = input("Enter note content: ").strip()

    if not content:
        print("Content cannot be empty.")
        return

    note = {
        "id": get_next_id(),
        "title": title,
        "topic": topic,
        "tags": tags,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    notes.append(note)
    save_notes()

    print("Note added successfully!")


def view_notes():
    if not notes:
        print("\nNo notes found.")
        return

    print("\n========== NOTES ==========")

    for index, note in enumerate(notes, start=1):

        note_id = note.get("id", index)
        title = note.get("title", "Untitled")
        topic = note.get("topic", "No Topic")
        tags = note.get("tags", [])
        content = note.get("content", "")
        created_at = note.get("created_at", "No date")

        tags_text = ", ".join(tags)

        if not tags_text:
            tags_text = "No tags"

        print("\n----------------------------")
        print(f"ID: {note_id}")
        print(f"Title: {title}")
        print(f"Topic: {topic}")
        print(f"Tags: {tags_text}")
        print(f"Created: {created_at}")
        print(f"Content: {content}")


def search_notes():
    if not notes:
        print("\nNo notes available to search.")
        return

    search_term = input("Search: ").strip().lower()

    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = []

    for note in notes:

        title = note.get("title", "").lower()
        topic = note.get("topic", "").lower()
        content = note.get("content", "").lower()
        tags = note.get("tags", [])

        tag_text = " ".join(tags).lower()

        if (
            search_term in title
            or search_term in topic
            or search_term in content
            or search_term in tag_text
        ):
            matches.append(note)

    if not matches:
        print("No matching notes found.")
        return

    print("\n========== SEARCH RESULTS ==========")

    display_notes(matches)


def view_notes_by_topic():
    if not notes:
        print("\nNo notes found.")
        return

    topic_input = input(
        "Enter topic: "
    ).strip().lower()

    if not topic_input:
        print("Topic cannot be empty.")
        return

    matches = []

    for note in notes:

        note_topic = note.get(
            "topic",
            ""
        ).lower()

        if note_topic == topic_input:
            matches.append(note)

    if not matches:
        print("No notes found for that topic.")
        return

    print(
        f"\n========== {topic_input.upper()} NOTES =========="
    )

    display_notes(matches)


def search_by_tag():
    if not notes:
        print("\nNo notes found.")
        return

    tag_input = input(
        "Enter tag: "
    ).strip().lower()

    if not tag_input:
        print("Tag cannot be empty.")
        return

    matches = []

    for note in notes:

        tags = note.get("tags", [])

        normalized_tags = []

        for tag in tags:
            normalized_tags.append(
                tag.lower()
            )

        if tag_input in normalized_tags:
            matches.append(note)

    if not matches:
        print("No notes found with that tag.")
        return

    print(
        f"\n========== TAG: {tag_input} =========="
    )

    display_notes(matches)


def display_notes(note_list):
    for note in note_list:

        note_id = note.get("id", "Unknown")
        title = note.get("title", "Untitled")
        topic = note.get("topic", "No Topic")
        tags = note.get("tags", [])
        content = note.get("content", "")
        created_at = note.get(
            "created_at",
            "No date"
        )

        tags_text = ", ".join(tags)

        if not tags_text:
            tags_text = "No tags"

        print("\n----------------------------")
        print(f"ID: {note_id}")
        print(f"Title: {title}")
        print(f"Topic: {topic}")
        print(f"Tags: {tags_text}")
        print(f"Created: {created_at}")
        print(f"Content: {content}")


def delete_note():
    if not notes:
        print("\nNo notes available.")
        return

    view_notes()

    try:
        note_id = int(
            input("\nEnter note ID to delete: ")
        )

        for note in notes:

            if note.get("id") == note_id:

                confirm = input(
                    f"Delete '{note['title']}'? (y/n): "
                ).strip().lower()

                if confirm != "y":
                    print("Deletion cancelled.")
                    return

                notes.remove(note)
                save_notes()

                print("Note deleted successfully!")
                return

        print("Note not found.")

    except ValueError:
        print("Please enter a valid note ID.")


def main():
    while True:
        show_menu()

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            add_note()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            search_notes()

        elif choice == "4":
            view_notes_by_topic()

        elif choice == "5":
            search_by_tag()

        elif choice == "6":
            delete_note()

        elif choice == "7":
            print("\nGoodbye!")
            break

        else:
            print(
                "Invalid choice. Please choose 1-7."
            )


if __name__ == "__main__":
    main()