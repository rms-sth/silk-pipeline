import asyncio
from dotenv import dotenv_values, load_dotenv

from fetch.crowd_strike_client import CrowdStrikeClient
from fetch.qualys_client import QualysClient
from normalize.crowd_strike import CrowdStrikeNormalizer
from normalize.qualys import QualysNormalizer
from process.data_processor import DataProcessor
from process.de_duplicator import DeDuplicator
from db.mongo_client import MongoDBClient
from visualize.visualizer import Visualizer

load_dotenv()
config = dotenv_values(".env")


class MainProcessor:
    def __init__(self):
        self.qualys_client = QualysClient(
            api_url=config["QUALYS_API_URL"],
            token=config["QUALYS_API_TOKEN"],
        )

        self.crowd_strike_client = CrowdStrikeClient(
            api_url=config["CROWDSTRIKE_API_URL"],
            token=config["CROWDSTRIKE_API_TOKEN"],
        )

        self.normalizers = {
            "crowd_strike": CrowdStrikeNormalizer(),
            "qualys": QualysNormalizer(),
        }

        self.de_duplicator = DeDuplicator()
        self.mongo_client = MongoDBClient(
            uri=config["MONGODB_URI"], db_name="silk_test1"
        )

    async def fetch_and_normalize_hosts(self):
        data_processor = DataProcessor(
            clients={
                "qualys": self.qualys_client,
                "crowd_strike": self.crowd_strike_client,
            },
            normalizers=self.normalizers,
            de_duplicator=self.de_duplicator,
        )

        return await data_processor.fetch_and_normalize_hosts()

    async def insert_hosts_to_mongodb(self, hosts):
        await self.mongo_client.create_indexes()
        await self.mongo_client.insert_hosts(hosts)

    async def visualize_hosts(self, hosts):
        visualizer = Visualizer(hosts)
        visualizer.plot_os_distribution()
        visualizer.plot_old_vs_new_hosts()

    async def run(self):
        de_duped_hosts = await self.fetch_and_normalize_hosts()
        await self.insert_hosts_to_mongodb(de_duped_hosts)
        await self.visualize_hosts(de_duped_hosts)


if __name__ == "__main__":
    main_processor = MainProcessor()
    asyncio.run(main_processor.run())
