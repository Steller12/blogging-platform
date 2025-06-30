class Post:
    _posts = []
    _id_counter = 1

    def __init__(self, title, body, is_published=False):
        self.id = Post._id_counter
        Post._id_counter += 1

        self.title = title
        self.body = body
        self.is_published = is_published
        Post._posts.append(self)

    # class helpers
    @classmethod
    def get_all(cls):
        return list(cls._posts)

    @classmethod
    def get_by_id(cls, post_id):
        return next((p for p in cls._posts if p.id == post_id), None)
