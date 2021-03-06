"""Module for generating GCP Projects."""
from faker import Faker


# pylint: disable=too-few-public-methods
class ProjectGenerator:
    """Generator for GCP Compute Engine data."""

    def __init__(self, account):
        """Initialize GCP Project Generator."""
        self.account = account
        self.fake = Faker()

    def generate_projects(self, num_projects=1):
        """Generate GCP project information."""
        projects = []
        for _ in range(num_projects):
            project_number = self.fake.ean13()  # pylint: disable=maybe-no-member
            project_id = '{}-{}-{}'.format(self.fake.word(),  # pylint: disable=maybe-no-member
                                           self.fake.word(),  # pylint: disable=maybe-no-member
                                           self.fake.ean8())  # pylint: disable=maybe-no-member
            labels = {
                self.fake.word(): self.fake.word(),  # pylint: disable=maybe-no-member
                self.fake.word(): self.fake.word(),  # pylint: disable=maybe-no-member
            }
            formatted_labels = ';'.join(f'{k}:{v}' for k, v in labels.items())
            project = {
                'Account ID': self.account,
                'Project': project_number,
                'Project Number': project_number,
                'Project ID': project_id,
                'Project Name': project_id,
                'Project Labels': formatted_labels
            }
            projects.append(project)

        return projects
