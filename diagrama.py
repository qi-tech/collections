from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.network import LoadBalancing
from diagrams.k8s.compute import Pod
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mssql
from diagrams.onprem.inmemory import Redis

graph_attr = {"fontsize": "65", "bgcolor": "transparent"}


with Diagram("BolePix", show=False, graph_attr=graph_attr):
    user = User("User")
    lb = LoadBalancing("LoadBalancer")
    sch = Scheduler("Scheduler")

    with Cluster("Gandalf"):
        gandalf_pod = Pod("Gandalf Pod")

    with Cluster("Pix"):
        qr_code_pod = Pod("QRCode Pod")
        pix_key = Pod("Pix Key Pod")
        pix_proxy = Pod("Pix Proxy Pod")

        pix_proxy - Server("Bacen")

    with Cluster("BankSlip"):
        pub_sub = PubSub("PubSub")

        with Cluster("BankSlip Service"):
            bs_pod = Pod("BankSlip Pod")

        with Cluster("BankSlip Workers"):
            handlers = [Pod("BankSlip Worker"), Pod("BankSlip Worker")]

        cip_server = Server("CIP")

    with Cluster("Database"):
        cache = Redis("cache")

        with Cluster("Database"):
            db_bs = Mssql("Bankslip db")
            db_qrcode = Mssql("Pix QRCode db")
            db_key = Mssql("Pix Key db")

    user >> Edge(label="~ 25000 \n ocorrências") >> lb >> gandalf_pod
    gandalf_pod >> bs_pod >> Edge(label="x 1000") >> pub_sub >> handlers
    handlers - pix_key
    handlers - qr_code_pod - pix_proxy
    sch >> Edge(label="~ 3 min.") >> bs_pod
    bs_pod >> cip_server

    bs_pod - db_bs
    qr_code_pod - db_qrcode
    pix_key - db_key
    handlers - db_bs

    db_bs - cache
    db_qrcode - cache
    db_key - cache
