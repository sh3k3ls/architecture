from diagrams import Cluster
from diagrams import Diagram

from diagrams.onprem.client import Users
from diagrams.azure.devops import Repos

from diagrams.aws.compute import EC2

from diagrams.aws.storage import S3

from diagrams.aws.management import CloudwatchEventTimeBased

from diagrams.aws.database import DynamodbTable

from diagrams.aws.integration import SimpleQueueServiceSqsQueue

from diagrams.aws.compute import LambdaFunction
from diagrams.onprem.compute import Server

from diagrams.aws.mobile import Amplify

from diagrams.generic.os import Android
from diagrams.generic.os import IOS

from diagrams.azure.devops import Pipelines
from diagrams.azure.devops import Artifacts

from diagrams.firebase.quality import CrashReporting
from diagrams.firebase.quality import Crashlytics
from diagrams.firebase.quality import PerformanceMonitoring

with Diagram("Shekels", show=True, direction="TB"):

    admin_user = Users("Admin User")
    operator_user = Users("Operator User")

    with Cluster("Admin"):
        admin_shekels = Amplify("Admin Shekels")
        admin_clients = Amplify("Admin Clients")

    with Cluster("Traders"):
        trader = Server("Operator")

    with Cluster("Users"):
        user = Server("User")

    with Cluster("API Gateway"):
        
        authorizer_system = LambdaFunction("authorizer_system")

        list_robots = LambdaFunction("list_robots")
        list_licences = LambdaFunction("list_robots")

        set_operation = LambdaFunction("set_operation")
        set_balance = LambdaFunction("set_balance")
        get_operation = LambdaFunction("get_operation")
        get_balance = LambdaFunction("get_balance")
        
        save_robot = LambdaFunction("save_robot")
        save_licence = LambdaFunction("save_licence")

    with Cluster("Database"):
        licences = DynamodbTable("licences")
        robots = DynamodbTable("robots")
        balance = DynamodbTable("balance")
        operations = DynamodbTable("operations")
        history = DynamodbTable("history")

    admin_user >> admin_shekels
    operator_user >> admin_clients

    trader >> authorizer_system >> set_operation

    user >> authorizer_system >> get_operation
    
    authorizer_system >> set_balance

    set_operation >> operations
    set_balance >> balance

    get_operation >> operations
    get_balance >> balance

    save_robot >> robots
    save_licence >> licences

    admin_clients >> authorizer_system

    admin_shekels >> authorizer_system >> save_licence
    authorizer_system >> save_robot
    authorizer_system >> get_operation
    authorizer_system >> get_balance

    authorizer_system >> list_robots
    authorizer_system >> list_licences