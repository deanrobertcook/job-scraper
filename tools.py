def dict_depth(d):
    """Return the depth of a dictionary"""
    if type(d) is dict:
        return 1 + (max(map(dict_depth, d.values())) if d else 0)
    return 0

def flatten_json(nested_json, exclude=[''], drop_lone_keys=False):
    """Flatten json object with nested keys into a single level.
        Credit: https://stackoverflow.com/a/57334325/1751834
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
            drop_lone_keys: if a dict key has no siblings, don't add it to the flattened key
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                #if drop_lone_keys and len(x.keys()) == 1 and dict_depth(x.values()) > 1: continue
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x



    flatten(nested_json)
    return out

## Tests
import unittest

class TestModule(unittest.TestCase):
    def test_dict_depth(self):
        self.assertEqual(dict_depth({'a': 'a_val'}), 1)

    def test_dict_depth(self):
        self.assertEqual(dict_depth({'a': {'b': 'b_val'}}), 2)

    def test_flatten_json(self):
        self.assertEqual(flatten_json({'a': {'b': 'b_val'}}), {'a_b': 'b_val'})

    def test_flatten_json_drop_lone_keys(self):
        self.assertEqual(flatten_json({'a': {'b': 'b_val'}}, drop_lone_keys=True), {'b': 'b_val'})


if __name__ == "__main__":
    unittest.main()
