# Randomize

- Python script that takes a JSON with a list and a JSON with the last result; it will choose an item from the list, avoiding the last result.

## How to use

```console
python3 randomize.py
```

- 1. Run the command above to create initial JSON files;
- 2. Edit `listToRandomize.json` with the result description and the data you need to randomize;
- 3. Run the command above again and the result will be printed to the screen.

### `--no-repeat` option

```console
python3 randomize.py --no-repeat
```

- Running the program with the flag `--no-repeat` will make it avoid all items that were already selected until the whole list is over;
- This option will also generate a nice log of the program execution in the file `alreadyRandomized.json`, thus generating an automatic report of an activity or process that needs random sorting to function.

### Saving the result

- Scripts `save_result_as_JSON.sh` and `save_result_as_TXT.sh` read data from the session JSON files and save it to the corresponding file format, allowing the session data to backed up.

#### Permissions

```console
chmod +x save_result_as_{JSON,TXT}.sh
```

- First add execution permission to the scripts.

---

#### As `.json`

```
./save_result_as_JSON.sh 'file_name'
```

- If `jq` is installed the result will the printed to the screen;
- Install it on `Debian` systems with

```console
sudo apt install -y jq
```

---

#### As `.txt`

```
./save_result_as_TXT.sh 'file_name'
```
