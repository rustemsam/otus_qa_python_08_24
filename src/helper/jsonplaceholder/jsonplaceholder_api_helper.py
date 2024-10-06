class JsonPlaceholderApiHelper:
    JSONPLACEHOLDER_API_URL = "https://jsonplaceholder.typicode.com/posts"

    def get_post(self, post_id):
        return f"{self.JSONPLACEHOLDER_API_URL}/{post_id}"

    def get_list_all_posts(self):
        return f"{self.JSONPLACEHOLDER_API_URL}"

    def create_post(self):
        return f"{self.JSONPLACEHOLDER_API_URL}"

    def update_post(self, post_id):
        return f"{self.JSONPLACEHOLDER_API_URL}/{post_id}"
