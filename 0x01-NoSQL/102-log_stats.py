#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
Database: logs, Collection: nginx, Display same as example
first line: x logs, x number of documents in this collection
second line: Methods
5 lines with method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
one line with method=GET, path=/status
improve by adding top 10 most present IPs in collection nginx
database logs
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')

    top_ips = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
