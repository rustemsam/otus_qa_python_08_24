class GectaroApiHelper:
    GECTARO_PROJECTS_API_URL = "https://api.gectaro.com/v1/projects"
    GECTARO_COMPANY_API_URL = "https://api.gectaro.com/v1/companies"

    def get_resource_requests(self, project_id):
        return f"{self.GECTARO_PROJECTS_API_URL}/{project_id}/resource-requests"

    def post_resource_requests(self, project_id):
        return f"{self.GECTARO_PROJECTS_API_URL}/{project_id}/resource-requests"

    def get_resource_request(self, project_id, resource_request_id):
        return f"{self.GECTARO_PROJECTS_API_URL}/{project_id}/resource-requests/{resource_request_id}"

    def put_resource_request(self, project_id, resource_request_id):
        return f"{self.GECTARO_PROJECTS_API_URL}/{project_id}/resource-requests/{resource_request_id}"

    def delete_resource_request(self, project_id, resource_request_id):
        return f"{self.GECTARO_PROJECTS_API_URL}/{project_id}/resource-requests/{resource_request_id}"

    def get_company_resource_requests(self, company_id):
        return f"{self.GECTARO_COMPANY_API_URL}/{company_id}/resource-requests"
