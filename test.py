import logging
import os
import pickle
import sys
from pogopvpdata import PokemonData


if __name__ == "__main__":

    logFormat = ('[%(asctime)s] [%(filename)s:%(lineno)3d] [%(levelname).1s] %(message)s')
    loglevel = logging.DEBUG if "-v" in sys.argv else logging.INFO
    logging.basicConfig(format=logFormat, level=loglevel)
    logger = logging.getLogger(__name__)

    picklefile = "data.pickle"
    data = None

    # bulbasaur test data
    great_b: list = [{'rank': 5, 'percentage': 99.839, 'pokemon': '2', 'form': '166', 'level': '39', 'cp': 1500},
                     {'rank': 1, 'percentage': 100.0, 'pokemon': '3', 'form': '169', 'level': '21', 'cp': 1498}]
    ultra_b: list = [{'rank': 33, 'percentage': 99.189, 'pokemon': '3', 'form': '169', 'level': '40', 'cp': 2498}, ]
    bulba_test: dict = {}
    bulba_test["name"]: str = "Bulbasaur"
    bulba_test["expected"]: tuple = (great_b, ultra_b)
    bulba_test["values"]: list = [1, 163, 0, 14, 11, 2]

    # ralts test data
    great_r: list = [{'rank': 1, 'percentage': 100.0, 'pokemon': '282', 'form': '298', 'level': '18', 'cp': 1496}, ]
    ultra_r: list = [{'rank': 2, 'percentage': 99.866, 'pokemon': '282', 'form': '298', 'level': '30', 'cp': 2494}, ]
    ralts_test: dict = {}
    ralts_test["name"]: str = "Ralts"
    ralts_test["expected"]: tuple = (great_r, ultra_r)
    ralts_test["values"]: list = [280, 292, 0, 15, 15, 1, 2]

    tests: list = [bulba_test, ralts_test]

    custom_values = False
    if len(sys.argv) > 1:
        try:
            mon, form, atk, de, sta, lvl, gender = [int(x) for x in sys.argv[1:8]]
            custom_values = True
        except Exception as e:
            logger.warning(f"Parsing error: {e}")
            logger.warning("Parsing custom values failed. Using builtin default tests.")
    else:
        logger.info("No values specified. Using builtin default tests.")

    try:
        with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), picklefile), "rb") as datafile:
            data = pickle.load(datafile)
            logger.info("loaded pickle'd data")
    except Exception as e:
        logger.warning("exception trying to load pickle'd data: {}".format(e))

    if not data:
        data = PokemonData(50, 50)

    # syntax:
    # getPoraclePvpInfo(self, mon, form, atk, de, sta, lvl)
    if not custom_values:
        logger.info("To run a custom test, pass the following values as arguments, separated by spaces: mon_id, "
                    "form_id, attack_iv, defense_iv, stamina_iv, level, gender. Example of the default test of"
                    "genderless Bulbasaur: python test.py 1 163 0 14 11 2 0")

        for test in tests:
            result = data.getPoraclePvpInfo(*test["values"])
            logger.info(f"{test['name']} test result: {result}")
            if result == test["expected"]:
                logger.info(f"{test['name']} test passed!")
            else:
                logger.warning(f"{test['name']} test received unexpected result!")
    else:
        gender = None if gender not in [1, 2, 3] else gender
        custom_test = data.getPoraclePvpInfo(mon, form, atk, de, sta, lvl, gender)
        logger.info(f"Custom test result: {custom_test}")

    try:
        with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), picklefile), "wb") as datafile:
            pickle.dump(data, datafile, -1)
            logger.info("Saved data to pickle file")
    except Exception as e:
        logger.warning("Failed saving to pickle file: {}".format(e))
