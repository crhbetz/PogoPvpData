import logging
import os
import pickle
import sys
from pogopvpdata import PokemonData


if __name__ == "__main__":

    logFormat = ('[%(asctime)s] [%(filename)s:%(lineno)3d] [%(levelname).1s] %(message)s')
    logging.basicConfig(format=logFormat, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    picklefile = "data.pickle"
    data = None

    great: list = [{'rank': 5, 'percentage': 99.839, 'pokemon': '2', 'form': '166', 'level': '39', 'cp': 1500},
                   {'rank': 1, 'percentage': 100.0, 'pokemon': '3', 'form': '169', 'level': '21', 'cp': 1498}]
    ultra: list = [{'rank': 33, 'percentage': 99.189, 'pokemon': '3', 'form': '169', 'level': '40', 'cp': 2498}, ]
    expected_result: tuple = (great, ultra)
    custom_values = False
    if len(sys.argv) > 1:
        try:
            mon, form, atk, de, sta, lvl = [int(x) for x in sys.argv[1:]]
            custom_values = True
        except Exception:
            logger.warning("Parsing custom values failed. Using a default Bulbasaur test: 0/14/11 @ Lvl 2 - this "
                           f"should return the following result: {expected_result}")
    else:
        logger.info("Using a default Bulbasaur test: 0/14/11 @ Lvl 2 - this should return the following result: "
                    f"{expected_result}")

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
                    "form_id, attack_iv, defense_iv, stamina_iv, level. Example of the default test: "
                    "python test.py 1 163 0 14 11 2")
        bulba_test = data.getPoraclePvpInfo(1, 163, 0, 14, 11, 2)
        logger.info(f"Bulbasaur test result: {bulba_test}")
        if bulba_test == expected_result:
            logger.info("Test passed!")
        else:
            logger.warning("Test received unexpected result!")
    else:
        custom_test = data.getPoraclePvpInfo(mon, form, atk, de, sta, lvl)
        logger.info(f"Custom test result: {custom_test}")

    try:
        with open("{}/{}".format(os.path.dirname(os.path.abspath(__file__)), picklefile), "wb") as datafile:
            pickle.dump(data, datafile, -1)
            logger.info("Saved data to pickle file")
    except Exception as e:
        logger.warning("Failed saving to pickle file: {}".format(e))
