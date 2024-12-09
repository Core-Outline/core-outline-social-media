from app_container.services.influencer_link_service import InfluencerLinkService


class InfluencerLink:
    def __init__(self):
        self.influencerLinkService = InfluencerLinkService()

    # def initialize(self, query_id, shortened_url, redirect_url, destination_url, conversions):
    #     self.data_source_name = data_source_name
    #     self.url = url
    #     self.username = username
    #     self.password = password
    #     self.user_id = user_id

    def create(self, influencer_link):
        return self.influencerLinkService.create_data_source(influencer_link)

    def get(self, influencer_link):
        return self.influencerLinkService.get_data_source_by_id(influencer_link)

    def fetch(self, influencer_link):
        return self.influencerLinkService.fetch_data_source_by_parameter(influencer_link)
