from flashcards.models import Section, WordPack, Quiz


def generate_content_for_section(section_id):
    try:
        section = Section.objects.get(pk=section_id)

        # Create WordPacks (Day 1 to Day 10)
        for i in range(1, 11):
            WordPack.objects.create(
                section=section,
                title=f"Day {i}",
                description=f"Vocabulary set for Day {i}",
                order=i
            )

        # Create Quizzes (Quiz 1 to Quiz 10)
        for i in range(1, 11):
            Quiz.objects.create(
                section=section,
                title=f"Quiz {i}",
                instructions=f"Answer the questions for Quiz {i}.",
                order=i
            )

        print(f"✅ Successfully generated 10 WordPacks and 10 Quizzes for Section ID {section_id}.")

    except Section.DoesNotExist:
        print(f"❌ Section with ID {section_id} does not exist.")
