import re

from django.shortcuts import render

from .forms import ListComparisonForm

input_delimiter_map = {
    "comma": ",",
    "newline": "\n",
    "semicolon": ";",
    "space": " ",
    "tab": "\t",
}

input_delimiter_map_re = {
    "comma": r",\s*",
    "newline": "\n",
    "semicolon": r";\s*",
    "space": r" +",
    "tab": "\t",
}

output_delimiter_map = {
    "comma": ", ",
    "newline": "\n",
    "semicolon": "; ",
    "space": " ",
    "tab": "\t",
}

item_enclosure_map = {
    "none": "x",
    "braces": "{x}",
    "brackets": "[x]",
    "double_quotes": '"x"',
    "parentheses": "(x)",
    "single_quotes": "'x'",
}

list_enclosure_map = {
    "none": ("", ""),
    "braces": ("{", "}"),
    "brackets": ("[", "]"),
    "double_quotes": ('"', '"'),
    "parentheses": ("(", ")"),
    "single_quotes": ("'", "'"),
}


def compare_lists(form_cleaned_data):
    list_a_raw = form_cleaned_data["list_a"]
    list_b_raw = form_cleaned_data["list_b"]

    # list_a = list_a_raw.split(input_delimiter_map[form_cleaned_data["input_delimiter"]])
    # list_b = list_b_raw.split(input_delimiter_map[form_cleaned_data["input_delimiter"]])
    list_a = re.split(
        input_delimiter_map_re[form_cleaned_data["input_delimiter"]], list_a_raw
    )
    list_b = re.split(
        input_delimiter_map_re[form_cleaned_data["input_delimiter"]], list_b_raw
    )

    list_a = [item.strip() for item in list_a if item.strip()]
    list_b = [item.strip() for item in list_b if item.strip()]

    if form_cleaned_data["sort_order"] == "alpha":
        list_a = sorted(list_a)
        list_b = sorted(list_b)

        set_a = set(list_a)
        set_b = set(list_b)

        a_minus_b = sorted(list(set_a - set_b))
        b_minus_a = sorted(list(set_b - set_a))
        intersection = sorted(list(set_a & set_b))
        union = sorted(list(set_a | set_b))

    elif form_cleaned_data["sort_order"] == "preserve":  # preserve existing order as is
        a_minus_b = []
        for item in list_a:
            if item not in list_b and item not in a_minus_b:
                a_minus_b.append(item)

        b_minus_a = []
        for item in list_b:
            if item not in list_a and item not in b_minus_a:
                b_minus_a.append(item)

        intersection = []
        for item in list_a:
            if item in list_b and item not in intersection:
                intersection.append(item)

        union = []
        for item in list_a:
            if item not in union:
                union.append(item)
        for item in list_b:
            if item not in union:
                union.append(item)

    else:
        raise ValueError(f"Invalid sort order: {form_cleaned_data["sort_order"]}")

    item_enclosure = item_enclosure_map[form_cleaned_data["item_enclosure"]]
    lists = [a_minus_b, b_minus_a, intersection, union]
    for list_ in lists:
        for i, item in enumerate(list_):
            list_[i] = item_enclosure.replace("x", item)

    output_delimiter = output_delimiter_map[form_cleaned_data["output_delimiter"]]

    results_notes = []
    results_notes.append("Duplicates were removed from the four output lists.")
    if form_cleaned_data["sort_order"] == "alpha":
        results_notes.append("Alphabetical sorting of results is case-sensitive.")

    list_enclosures = list_enclosure_map[form_cleaned_data["list_enclosure"]]

    return {
        "list_a": input_delimiter_map[form_cleaned_data["input_delimiter"]].join(
            list_a
        ),
        "list_b": input_delimiter_map[form_cleaned_data["input_delimiter"]].join(
            list_b
        ),
        "a_minus_b": list_enclosures[0]
        + output_delimiter.join(a_minus_b)
        + list_enclosures[1],
        "b_minus_a": list_enclosures[0]
        + output_delimiter.join(b_minus_a)
        + list_enclosures[1],
        "intersection": list_enclosures[0]
        + output_delimiter.join(intersection)
        + list_enclosures[1],
        "union": list_enclosures[0] + output_delimiter.join(union) + list_enclosures[1],
        "list_a_count": len(list_a),
        "list_b_count": len(list_b),
        "a_minus_b_count": len(a_minus_b),
        "b_minus_a_count": len(b_minus_a),
        "intersection_count": len(intersection),
        "union_count": len(union),
        "results_notes": " ".join(results_notes),
    }


def index(request):
    if request.method == "POST":
        form = ListComparisonForm(request.POST)
        if form.is_valid():
            # list_a = form.cleaned_data["list_a"]
            # list_b = form.cleaned_data["list_b"]
            # input_delimiter = form.cleaned_data["input_delimiter"]
            # output_delimiter = form.cleaned_data["output_delimiter"]
            # sort_order = form.cleaned_data["sort_order"]

            result = compare_lists(form.cleaned_data)

            return render(
                request, "comparator/result.django", {"form": form, "result": result}
            )
        else:
            print(form.errors)

    else:
        form = ListComparisonForm()

    return render(request, "comparator/index.django", {"form": form})
