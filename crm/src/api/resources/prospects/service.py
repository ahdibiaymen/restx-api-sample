from src import exceptions
from src.models import Prospect


class ProspectService:
    def __init__(self, name=None, company=None):
        self.name_filter = name
        self.company_filter = company

    def check_filters(self):
        return any([self.name_filter, self.company_filter])

    def get_prospects(self):
        # without filters
        if not self.check_filters():
            return [prospect for prospect in Prospect.select()]
        else:
            # with filters
            prospects_query = Prospect.select()
            if self.name_filter:
                prospects_query = prospects_query.where(
                    Prospect.name == self.name_filter
                )
            if self.company_filter:
                prospects_query = prospects_query.where(
                    Prospect.company == self.company_filter
                )

            return [product for product in prospects_query]

    def create_new_prospect(self, prospect_info):
        # search for the prospect if exists
        prospect = (
            Prospect.select()
            .where(Prospect.name == prospect_info["name"])
            .first()
        )
        if prospect:
            raise exceptions.AlreadyExist(
                prospect_name=prospect_info["name"],
                operation="CREATE_NEW_PROSPECT",
            )

        # create new product
        prospect = Prospect(**prospect_info)
        prospect.save()
        return prospect
