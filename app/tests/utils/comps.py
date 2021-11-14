from app.tests.constants import (
    FAKE_COMP_DESC,
    DEFAULT_TEST_START,
    DEFAULT_TEST_END,
    DEFAULT_FAKE_COMP_CSV_OUTPUT,
    DEFAULT_FAKE_COMP_ENTRY_CSV_OUTPUT,
)
from collections import defaultdict 
from datetime import timedelta, datetime 
from random import choice, shuffle  
from app.tests.utils.files import FileWriter
import pprint 

class CompetitionEntryGenerator:

    def generate_csv_comp_entries(
        self, 
        fake_comps, 
        fake_backtests,
        fake_users, 
    ):

        # user id to user information 
        reverse_user_idx = {}
        for user in fake_users: 
            reverse_user_idx[user['id']] = user 
        
        # backtest owner username to backtests 
        reverse_back_idx = defaultdict(list)
        for backtest in fake_backtests: 
            owner = backtest['owner']
            reverse_back_idx[reverse_user_idx[owner]['username']].append(backtest)

        ret = []
        csv_info = [] 
        
        for comp in fake_comps: 

            for username in reverse_back_idx: 
                poss = reverse_back_idx[username]
                shuffle(poss)
                backtest_submission = None 
                for backtest in poss: 
                    if backtest['score'] >= 0:
                        backtest_submission = backtest 
                        break 

                ret.append({
                    'comp_id': comp['id'],
                    'owner': username, 
                    'backtest_id': backtest_submission['id'],
                    'backtest_algo': backtest_submission['algo'],
                    'result': backtest_submission['result'],
                    'score': backtest_submission['score'],
                    'code_snapshot': backtest_submission['code'],
                    'test_interval': backtest_submission['test_interval'],
                    'test_start': backtest_submission['test_start'],
                    'test_end': backtest_submission['test_end']
                })

                csv_info.append([
                    str(comp['id']),
                    username, 
                    str(backtest_submission['id']),
                    str(backtest_submission['algo']),
                    backtest_submission['result'],
                    str(backtest_submission['score']),
                    backtest_submission['code'],
                    backtest_submission['test_interval'],
                    backtest_submission['test_start'],
                    backtest_submission['test_end']
                ])
        
        FileWriter.write_csv_to_path(
            DEFAULT_FAKE_COMP_ENTRY_CSV_OUTPUT, 
            csv_info,
        )

        return ret 

class CompetitionGenerator:

    def __init__(self):
        self.titles = [
            "very long competition title that is a test for stress testing",
            "another competition title for test test test test test test",
            "yet another test test test test test test test test test test test",
        ]

        with open(FAKE_COMP_DESC) as f: 
            self.desc = f.read() 
        
        self.end_time = str(datetime.now() + timedelta(days=30))

        self.test_start = DEFAULT_TEST_START
        self.test_end = DEFAULT_TEST_END 

        self._curr_id = 1 
    
    def generate_csv_user_comps(self, fake_users, num_comps):

        ret = [] 
        csv_info = [] 

        for user in fake_users: 
            username = user['username']

            title = choice(self.titles)
            ret.append({
                "id": self._curr_id, 
                'title': title, 
                'description': self.desc, 
                'owner': username, 
                'end_time': self.end_time,
                'test_start': self.test_start, 
                'test_end': self.test_end, 
            })
            csv_info.append([
                title, 
                self.desc, 
                username, 
                self.end_time, 
                self.test_start, 
                self.test_end, 
            ])
            self._curr_id += 1

        FileWriter.write_csv_to_path(
            DEFAULT_FAKE_COMP_CSV_OUTPUT,
            csv_info,
        )

        return ret 
