class LessonController(object):
    def __init__(self, data):
        super(LessonController, self).__init__()
        self.data = data

    def save_parsed_data(self):
        for item in self.data:
            Lesson.objects.create(
                subject=item.subject,
                teacher=item.teacher,

            )
