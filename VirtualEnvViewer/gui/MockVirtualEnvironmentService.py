__author__ = 'mario'
from VirtualEnvironmentService import VirtualEnvironmentService

class MockVirtualEnvironmentService(VirtualEnvironmentService):

    def __init__(self, b):
        super(MockVirtualEnvironmentService, self).__init__(b)


    def get_elevation_map(self):
        return self._parse_elevation_map_data({
  "environment_configuration": [
    [
      50,
      50
    ],
    [
      100,
      100
    ]
  ],
  "virtual_objects": [
    {
      "cells": [
        [
          2,
          2,
          333
        ]
      ]
    }
  ]
})

