class Config:

    @property
    def supported_keys(self):
        return SUPPORTED_KEYS

SUPPORTED_KEYS = [
    {
        "domain" : "Reliability",
        "keys" : [
            "bugs",
            "reliability_rating",
            "reliability_remediation_effort"
        ]
    },
    {
        "domain" : "Security",
        "keys" : [
            "vulnerabilities",
            "security_hotspots",
            "security_rating",
            "security_remediation_effort",
            "security_review_rating"
        ]
    },
    {
        "domain" : "Maintainability",
        "keys" : [
            "code_smells",
            "development_cost",
            "effort_to_reach_maintainability_rating_a",
            "sqale_rating",
            "sqale_index",
            "sqale_debt_ratio"
        ]
    },
    {
        "domain" : "Duplications",
        "keys" : [
            "duplicated_blocks",
            "duplicated_files",
            "duplicated_lines",
            "duplicated_lines_density",
            "duplications_data"
        ]
    },
    {
        "domain" : "Coverage",
        "keys" : [
            "coverage",
            "branch_coverage",
            "conditions_to_cover",
            "executable_lines_data",
            "line_coverage",
            "lines_to_cover",
            "skipped_tests",
            "uncovered_conditions",
            "test_failures",
            "test_errors",
            "test_success_density",
            "test_execution_time"
        ]
    },
    {
        "domain" : "Size",
        "keys" : [
            "classes",
            "comment_lines",
            "comment_lines_data",
            "comment_lines_density",
            "directories",
            "files",
            "functions",
            "generated_lines",
            "generated_ncloc",
            "lines",
            "ncloc",
            "ncloc_data",
            "projects",
            "statements"
        ]
    },
    {
        "domain" : "Issues",
        "keys" : [
            "violations",
            "open_issues",
            "reopened_issues",
            "confirmed_issues",
            "false_positive_issues",
            "wont_fix_issues"
        ]
    },
    {
        "domain" : "Complexity",
        "keys" : [
            "complexity",
            "cognitive_complexity",
            "class_complexity",
            "file_complexity",
            "function_complexity",
            "complexity_in_classes",
            "complexity_in_functions"
        ]
    },
    {
        "domain" : "Releaseability",
        "keys" : [
            "alert_status",
            "quality_gate_details"
        ]
    }
]
