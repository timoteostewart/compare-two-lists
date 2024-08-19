from django import forms


class CustomRadioSelect(forms.RadioSelect):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        # Setting the ID for each radio button
        if attrs is None:
            attrs = {}

        attrs["id"] = f"id_{name}_{value}"

        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )

        # Disabling specific options if needed
        if value in ["numeric_prefix", "numeric_suffix"]:
            option_dict["attrs"]["disabled"] = "disabled"

        return option_dict


class DisabledRadioSelect(forms.RadioSelect):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value in ["numeric_prefix", "numeric_suffix"]:
            option_dict["attrs"]["disabled"] = "disabled"
        return option_dict


class ListComparisonForm(forms.Form):
    INPUT_DELIMITER_CHOICES = [
        ("comma", "Comma"),
        ("newline", "Newline"),
        ("semicolon", "Semicolon"),
        ("space", "Space"),
        ("tab", "Tab"),
    ]

    OUTPUT_DELIMITER_CHOICES = [
        ("comma", "Comma"),
        ("newline", "Newline"),
        ("semicolon", "Semicolon"),
        ("space", "Space"),
        ("tab", "Tab"),
    ]

    ITEM_ENCLOSURE_CHOICES = [
        ("none", "None"),
        ("braces", "Braces {x}"),
        ("brackets", "Brackets [x]"),
        ("double_quotes", 'Double quotes "x"'),
        ("parentheses", "Parens (x)"),
        ("single_quotes", "Single quotes 'x'"),
    ]

    LIST_ENCLOSURE_CHOICES = [
        ("none", "None"),
        ("braces", "Braces {x}"),
        ("brackets", "Brackets [x]"),
        ("double_quotes", 'Double quotes "x"'),
        ("parentheses", "Parens (x)"),
        ("single_quotes", "Single quotes 'x'"),
    ]

    SORT_CHOICES = [
        ("preserve", "Preserve order"),
        ("alpha", "Alphabetical"),
        ("numeric_prefix", "Numeric prefix"),
        ("numeric_suffix", "Numeric suffix"),
    ]

    SPECIAL_OUTPUT_FORMAT_CHOICES = [
        ("none", "None"),
        ("python_list", "Python list"),
    ]

    list_a = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control list-textarea list-textarea-input list-a-class",
                "columns": 40,
                "rows": 3,
            }
        ),
        label="List A",
    )
    list_b = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control list-textarea list-textarea-input list-b-class",
                "columns": 40,
                "rows": 3,
            }
        ),
        label="List B",
    )

    input_delimiter = forms.ChoiceField(
        choices=INPUT_DELIMITER_CHOICES,
        widget=CustomRadioSelect(attrs={"class": "form-check-input option-choice"}),
        label="Delimiter",
        initial="newline",
    )

    output_delimiter = forms.ChoiceField(
        choices=OUTPUT_DELIMITER_CHOICES,
        widget=CustomRadioSelect(attrs={"class": "form-check-input option-choice"}),
        label="Delimiter",
        initial="newline",
    )

    item_enclosure = forms.ChoiceField(
        choices=ITEM_ENCLOSURE_CHOICES,
        widget=CustomRadioSelect(attrs={"class": "form-check-input option-choice"}),
        label="Item enclosure",
        initial="none",
    )

    list_enclosure = forms.ChoiceField(
        choices=LIST_ENCLOSURE_CHOICES,
        widget=CustomRadioSelect(attrs={"class": "form-check-input option-choice"}),
        label="List enclosure",
        initial="none",
    )

    sort_order = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=DisabledRadioSelect(attrs={"class": "form-check-input option-choice"}),
        label="Sorting",
        initial="preserve",
    )

    special_output_format = forms.ChoiceField(
        choices=SPECIAL_OUTPUT_FORMAT_CHOICES,
        widget=CustomRadioSelect(
            attrs={"class": "form-check-input option-choice", "disabled": "disabled"}
        ),
        label="Special format",
        initial="none",
        required=False,
    )
