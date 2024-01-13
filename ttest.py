from singletons import SharedData


class ClassA:
    shared_dict = SharedData.dictionary

class ClassB:
    shared_dict = SharedData.dictionary

# Modify the shared dictionary
SharedData.dictionary["key1"] = "new_value"


# Print the dictionary in ClassA and ClassB
print(ClassA.shared_dict)  # Output: {'key1': 'new_value', 'key2': 'value2'}
print(ClassB.shared_dict)  # Output: {'key1': 'new_value', 'key2': 'value2'}

print(id(SharedData.dictionary))
print(id(ClassA.shared_dict))
print(id(ClassB.shared_dict))
