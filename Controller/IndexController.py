#! encoding: utf-8

from typing import Dict
import json
from Controller.BaseController import BaseController


class IndexController(BaseController):

    def __init__(self, application, request, **kwargs):
        super(IndexController, self).__init__(application, request, **kwargs)
        

    def get(self):
        self.to_respond(0, "success", {})

 