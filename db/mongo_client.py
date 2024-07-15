from typing import Any, Dict, List

import motor.motor_asyncio

class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["hosts"]

    async def insert_hosts(self, hosts: List[Dict[str, Any]]) -> None:
        for host in hosts:
            query = {
                "ip_addresses": {"$in": host["ip_addresses"]},
                "mac_address": host["mac_address"],
            }

            existing_host = await self.collection.find_one(query)

            update_fields = {
                "platform": host["platform"],
                "hostnames": host["hostnames"],
                "os": host["os"],
                "last_seen": host["last_seen"],
                "location": host["location"],
                "software": host["software"],
                "open_ports": host["open_ports"],
            }

            if existing_host:
                # Prepare the update operations
                update_set_fields = {}
                for key, value in update_fields.items():
                    if key not in existing_host or existing_host[key] is None:
                        update_set_fields[key] = value

                if update_set_fields:
                    await self.collection.update_one(query, {"$set": update_set_fields})
            else:
                await self.collection.update_one(
                    query,
                    {
                        "$setOnInsert": {
                            "host_id": host["host_id"],
                            "ip_addresses": host["ip_addresses"],
                            "mac_address": host["mac_address"],
                        },
                        "$set": update_fields,
                    },
                    upsert=True,
                )

    async def get_hosts(self) -> List[Dict[str, Any]]:
        cursor = self.collection.find()
        return await cursor.to_list(length=None)

    async def de_dupe_hosts(self) -> None:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "ip_addresses": "$ip_addresses",
                        "mac_address": "$mac_address",
                    },
                    "uniqueIds": {"$addToSet": "$_id"},
                    "count": {"$sum": 1},
                }
            },
            {"$match": {"count": {"$gt": 1}}},
            {"$unwind": "$uniqueIds"},
            {"$sort": {"_id": 1}},
            {"$group": {"_id": "$_id", "idsToRemove": {"$push": "$uniqueIds"}}},
            {
                "$project": {
                    "idsToRemove": {
                        "$slice": [
                            "$idsToRemove",
                            1,
                            {"$subtract": [{"$size": "$idsToRemove"}, 1]},
                        ]
                    }
                }
            },
        ]

        async for doc in self.collection.aggregate(pipeline):
            if doc["idsToRemove"]:
                await self.collection.delete_many({"_id": {"$in": doc["idsToRemove"]}})

        print("Deduplication complete.")

    async def create_indexes(self):
        await self.collection.create_index(
            [("ip_addresses", 1), ("mac_address", 1)], unique=True
        )

    async def connect(self):
        await self.client.admin.command("ping")

    async def close(self):
        self.client.close()
