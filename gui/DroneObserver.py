from abc import ABCMeta, abstractmethod


class DroneObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_drone_pose(self, drone_pose):
        pass

    @abstractmethod
    def update_virtual_environment(self, elevation_map, existing_objects):
        pass
