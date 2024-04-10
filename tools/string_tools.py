from re import sub

class StringTools:
    @staticmethod
    def deduplicate(strings):
        unique_strings = set()
        deduplicated_list = []
        for string in strings:
            normalized_string = sub(
                r"[^a-zA-Z0-9À-ÿ]", "", " ".join(string.lower().split()))
            if normalized_string not in unique_strings:
                deduplicated_list.append(string)
                unique_strings.add(normalized_string)
        return deduplicated_list

    @staticmethod
    def join_text(item_list, separator_1=" and ", separator_2=", "):
        assert isinstance(separator_1, str) and isinstance(separator_2, str)
        text = ""
        for i in range(0, len(item_list)):
            text += str(item_list[i])
            if i == len(item_list) - 1:
                return text
            elif i == len(item_list) - 2:
                text += separator_1
            else:
                text += separator_2
