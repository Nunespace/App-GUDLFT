from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {'email': "kate@shelifts.co.uk"})

    @task
    def book_page(self):
        self.client.get("/book/Spring Festival/She Lifts")

    @task
    def book(self):
        data = {
            "club": "She Lifts",
            "competition": "Spring Festival",
            "places": 6,
        }
        self.client.post('/purchasePlaces', data)

    @task
    def logout(self):
        self.client.get('/logout')
