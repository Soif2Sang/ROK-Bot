import flet as ft

from utils.Components.card import GenerateCard, SimpleCard
from utils.schemas.emulator_schemas import TaskProduceMaterialsSchema

from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_material import FletRowMaterial


class PageMaterials(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskProduceMaterialsSchema = self.tasks.produce_materials

        keys = [
            "first_choice",
            "second_choice",
            "third_choice",
            "fourth_choice",
            "fifth_choice",
        ]

        self.add_control(
            SimpleCard(content="Choose material to produce with the blacksmith.")
        )

        for key in keys:
            self.add_control(
                FletRowMaterial(
                    key=key,
                    context=self.context,
                )
            )