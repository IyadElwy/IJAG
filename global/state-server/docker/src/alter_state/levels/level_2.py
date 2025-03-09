from kubernetes import client, config
from utils.json_state_helpers import get_current_game_state


class Level2:
    def __init__(self, level_key: str):
        config.load_incluster_config()
        self.v1_client = client.CoreV1Api()
        self.level_key = level_key
        self.alter_cluster()
        while True:
            finished_altering_state = self.check_alter_status()
            if finished_altering_state:
                return

    def alter_cluster(self):
        current_game_state = get_current_game_state()
        last_level_namespace = current_game_state.currentState.level.get("1").levelKey
        self.v1_client.delete_namespace(name=last_level_namespace)
        # namespace_body = client.V1Namespace(
        #     metadata=client.V1ObjectMeta(
        #         name=self.level_key, labels={"name": self.level_key}
        #     )
        # )
        # self.v1_client.create_namespace(body=namespace_body)
        pass

    def check_alter_status(self) -> bool:
        # namespace = self.v1_client.read_namespace(self.level_key)
        # print(namespace)
        return True
