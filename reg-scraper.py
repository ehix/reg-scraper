import json
from multiprocessing.pool import ThreadPool

import clean_air_zone as caz
import vehicle_excise_duty as ved


class ResultsHandler():
    def __init__(self, json=False):
        self.results = dict()
        self.json = json

    def update(self, output):
        self.results.update(output)

    def get(self):
        if self.json:
            return json.dumps(self.results, indent=4)
        return self.results


class ConfigHandler():
    def __init__(self, args):
        self.args = args

    @classmethod
    def from_config(cls):
        scripts = {"caz": caz.run, "ved": ved.run}
        with open("./config.json") as f:
            config = json.load(f)

        # could imagine reg being a param?
        reg = config.pop("reg")
        args = []
        for k, v in config.items():
            v.update({"reg": reg})
            args.append(tuple([scripts.get(k), v]))
        return cls(args)


if __name__ == '__main__':
    # print(caz.run)
    # args = Config.consume(file)

    results = ResultsHandler(json=True)
    # create and configure the thread pool
    # print(everything)
    # for i in everything:
    #     print(i[1].values())
    config = ConfigHandler.from_config()
    with ThreadPool(2) as pool:
        _ = [pool.apply_async(func, args=args.values(
        ), callback=results.update) for func, args in config.args]
        pool.close()
        # wait for all issued tasks to complete
        pool.join()

    print(results.get())
