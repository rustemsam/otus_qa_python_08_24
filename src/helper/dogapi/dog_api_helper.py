class DogApiHelper:
    DOG_API_BREEDS_URL = "https://dog.ceo/api/breeds"
    DOG_API_BREED_URL = "https://dog.ceo/api/breed/"

    def get_random_dog_image_url(self):
        return f"{self.DOG_API_BREEDS_URL}/image/random"

    def get_list_all_breeds_url(self):
        return f"{self.DOG_API_BREEDS_URL}/list/all"

    def get_list_images_by_breed_url(self, breed):
        return f"{self.DOG_API_BREED_URL}{breed}/images"

    def get_sub_breed_list_url(self, breed):
        return f"{self.DOG_API_BREED_URL}{breed}/list"
