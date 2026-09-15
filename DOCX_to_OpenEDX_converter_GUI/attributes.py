class library_attributes():
    def __init__(self):
        self.url_name="library" 
        self.xblock_family="xblock.v1" #it needs "-"
        self.video_auto_advance="false" 
        self.graded="false" 
        self.tags="[]" 
        self.edxnotes="false" 
        self.use_latex_compiler="false" 
        self.video_bumper="{}" 
        self.course_edit_method="Studio" 
        self.show_correctness=None
        self.static_asset_path="" 
        self.hide_from_toc="false" 
        self.in_entrance_exam="false" 
        self.showanswer=None
        self.display_name="Тест" 
        self.group_access="{}" 
        self.video_speed_optimizations="true" 
        self.graceperiod="null" 
        self.rerandomize="never" 
        self.user_partitions="[]" 
        self.show_reset_button="false" 
        self.days_early_for_beta="null" 
        self.max_attempts="null" 
        self.self_paced="false" 
        self.visible_to_staff_only="false" 
        self.org="LETI" 
        self.library="Test_Library"

class problem_attributes():
    def __init__(self):
        self.course_edit_method="Studio" 
        self.display_name="Вопрос" 
        self.markdown="null" 
        self.max_attempts="1" 
        self.rerandomize="per_student" 
        #self.show_correctness="always" 
        self.show_correctness=None
        self.showanswer="never" 
        self.video_speed_optimizations="true" 
        self.weight="1.0"
        self.show_reset_button="false"
        self.tolerance="1%"
        self.submission_wait_seconds = None

class default_problem_attributes(problem_attributes):
    def __init__(self):
        super().__init__()
        self.reg_type_t = None
        self.reg_type_m = None
        self.trailing_text_t = None
        self.trailing_text_m = None
        self.trailing_text_n = None

    def copy(self, other, type = ""):
        other.course_edit_method = self.course_edit_method 
        other.display_name = self.display_name 
        other.markdown = self.markdown 
        other.max_attempts = self.max_attempts 
        other.rerandomize = self.rerandomize 
        other.show_correctness = self.show_correctness 
        other.showanswer = self.showanswer
        other.video_speed_optimizations = self.video_speed_optimizations
        other.weight = self.weight
        other.show_reset_button = self.show_reset_button
        other.tolerance = self.tolerance
        other.submission_wait_seconds = self.submission_wait_seconds
        if type == "t":
            other.reg_type = self.reg_type_t
            other.trailing_text = self.trailing_text_t
        elif type == "m":
            other.reg_type = self.reg_type_m
            other.trailing_text = self.trailing_text_m
        elif type == "n":
            other.trailing_text = self.trailing_text_n


class refined_problem_attributes(problem_attributes):
    def __init__(self):
        super().__init__()
        self.reg_type = None
        self.trailing_text = None



