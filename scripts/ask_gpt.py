# import os
import openai
import pyperclip
from pprint import pprint

class GPTAsker:
    def __init__(self, key_path="openai_api_key.config", rewrite_article=False, add_more=None):
        openai.api_key_path = key_path
        self.system_message = "You will be provided with an article or story.\n\nYou are writing like a financial analyst.\n\nAfter you have written something, always go through and replace the following words with other words prior to outputting your final response: delve, elevate, tapestry, resonate, multifaceted, beacon, interplay, paramount, orchestrate, annals, enigma, indelible, whimsical, bespoke, nuanced, dynamic, crucial, key, juncture.\n\nFirst, if the article is over 600 words, let me know the current length.  e.g. \"Current Length: 601\"\n\nPlease determine the stock symbol for which the story is intended. If none exists, return:\n\n\"Story Equity Symbol: MACROAXIS\"\n(Specify equity symbol for which this story is intended.)\n\n---\n\nPlease determine the best Story Category based on the article content. Here are the choices to pick from:\nTechnical Analysis\nFundamental Analysis\nHype\nPerspective\nProduct Development\nForecasting\nValuation\nAdvice\nVolatility\nLeverage Analysis\nRisk Management\nMarket Trends\nBlog\n(Specify category this story is applicable for.)\n\n---\n\nStory Coverage\nServices\nCryptocurrency\nAgriculture\nConstruction\nGoverment\nMining\nRetail\nEntertainment\nFood\nFinance\nOther\nManufacturing\nTechnology\nIndustry\nDrugs\nCars\nIdeas\nTechnical Indicator\nPredictive Analysis\nFundamental Ratio\nMomentum And Patterns\n(Specify coverage type for which this story is intended.)\n\n---\n\nPlease extract the title. If necessary, modify the title to make it more readable, between 40 and 120 characters, and/or SEO friendly, and remove colons. If the title is not in English, please translate it to English.\n\n---\n\nWrite an abstract (Provide abstract of the story including main idea and key points you are covering.)\n\nWrite a summary (Provide short summary of the story. We recommend this to be two or three small paragraphs).\n\n---\n\nIdentify any \"non-standard punctuation,\" by which I mean things such as curly quotes (‘’“”) used in the story.\nIf there are any formatted quotes (characters in the set [‘’“”]), please let me know where they are so I can change them to basic quotes and apostrophes ([\'\"]).\n\n---\n\nAlso, let me know whether there are any typos or other (spelling, grammar, etc.) issues that need to be fixed.\n\n---\n\ne.g.:\n\nCurrent Length: 835\n\nStory Equity Symbol: MACROAXIS\n\nStory Category: Market Trends\n\nStory Coverage: Finance\n\nTitle: {title}\n\nAbstract: {abstract}\n\nSummary: {summary}\n\nNon-standard punctuation: None\n\nGrammar/Spelling issues: None"
        # the story categories that can't actually be used without breaking the site: Insider Trading, Thematic Ideas, Description
        if rewrite_article:
            self.system_message += "\n\n---\n\nthen, rewrite the article.\nkeep the gist of the article\nmake it shorter, not much more than 500 words. remove things that aren't relevant"
        if add_more:
            self.system_message += f"\n\n---\n\nPlease change the following:\n\n{add_more}"
        self.original_response = None
        
    def ask_gpt(self, original_article_content: str):
        self.request = {
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [
                {
                    "role": "system",
                    "content": self.system_message
                },
                {
                    "role": "user",
                    "content": original_article_content # "[insert article here or extract it from file]"
                }
            ],
            "temperature": 1,
            "max_tokens": 2000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        original_response = openai.ChatCompletion.create(**self.request)
        self.original_response = original_response["choices"][0]["message"]["content"]
        return original_response
    
    def get_original_response(self):
        """ Returns the original response from OpenAI's API parses the document.
        """
        return self.original_response

    
    
    def parse_response(self):
        """ Parses the response from OpenAI's API and returns a dictionary with the following keys:
        - story_metadata
        - abstract
        - summary
        """
        if not self.original_response:
            raise Exception("You need to call ask_gpt() first. This method depends on the original response from OpenAI's API.")
        
        parsed_response = {}
        for block in self.original_response.split("\n\n"):
            if ": " in block:
                key, value = block.split(": ", 1)
                key = key.split(" ")[-1].lower() # e.g. "Story Length: 910" -> "length"
                parsed_response[key] = value
            else:
                # TODO: sometimes, the first block is just a number, e.g. "910"
                print('Warning: Block did not contain expected format -', block)

        # parsed_response["length"] = self.original_response.split("\n")[0].split(": ")[1] # "Story Length: 910"
        # parsed_response["symbol"] = self.original_response.split("\n")[2].split(": ")[1]
        # parsed_response["category"] = self.original_response.split("\n")[4].split(": ")[1]
        # parsed_response["coverage"] = self.original_response.split("\n")[6].split(": ")[1]
        # parsed_response["title"] = self.original_response.split("\n")[8].split(": ")[1]
        # parsed_response["abstract"] = self.original_response.split("\n")[10].split(": ")[1]
        # parsed_response["summary"] = self.original_response.split("\n")[12].split(": ")[1]

        self.parsed_response = parsed_response
        return parsed_response
    
    def print_uncopyable_response(self):
        """ Prints the response from OpenAI's API.
        """
        if not self.original_response:
            raise Exception("You need to call ask_gpt() first. This method depends on the original response from OpenAI's API.")
        # print(self.original_response)
        # pprint(self.parsed_response)
        # pprint the parsed response, but only the keys that cannot be copied: length, symbol, category, coverage
        print('\n'.join(f"{k}: {v}" for k, v in self.parsed_response.items() if k in ["length", "symbol", "category", "coverage"]))

    def print_copyable_response(self):
        """ Prints the response from OpenAI's API.
        Print the parts of the response that were copied in case the user didn't save them.
        """
        if not self.original_response:
            raise Exception("You need to call ask_gpt() first. This method depends on the original response from OpenAI's API.")
        print("Here are the parts of the response that were copied to the clipboard:")
        print('\n'.join(f"{k}: {v}" for k, v in self.parsed_response.items() if k not in ["length", "symbol", "category", "coverage"]))
    
    def copy_parsed_response(self):
        """ Copies the response parts from OpenAI's API to the clipboard.
        """
        if not self.original_response:
            raise Exception("You need to call ask_gpt() first. This method depends on the original response from OpenAI's API.")
        
        print("Copying the equity symbol to the clipboard.")
        pyperclip.copy(self.parsed_response["symbol"])

        print("Copying the title to the clipboard clipboard. Please press any key to continue...")
        input()
        pyperclip.copy(self.parsed_response["title"])

        print("Copying the abstract to the clipboard. Please press any key to continue...")
        input()
        pyperclip.copy(self.parsed_response["abstract"])

        print("Copying the summary to the clipboard. Please press any key to continue...")
        input()
        pyperclip.copy(self.parsed_response["summary"])

    def test_all(self, test_article_content: str = None):
        """ Tests all methods in this class.
        """
        if test_article_content is None:
            original_article_content = """5 Golden Rules for Successful Forex Trading for Beginners 
 
    The global foreign exchange market is the largest financial market in the world. Daily volume averaged around $7.5 trillion in 2022, making it – by a considerable distance – the world’s most liquid market. While much of forex trading is conducted by banks and financial institutions, individuals are increasingly using online trading platforms to trade forex pairs. We are experiencing a boom in casual traders, those who are interested in trading as a hobby or as a means to secure more income. There are risks, of course, and nobody is guaranteed success in forex trading. But the abundance of new smart trading tools and educational resources means that the average retail trader can be successful.  
    However, risks are at the most heightened for novice traders. If you are unsure of what you are doing in forex, you’re more likely experience losses than profits. In light of that, we wanted to present five general rules for beginners that will help them on their way. These rules are more focused on trading ethos than specific trading strategies. But if you heed the advice below, you can have a positive perspective as you begin your forex trading journey. 
    1.	Understand the Nature of Forex Markets 
    Forex trading has unique qualities that are not present in other trading products. While parts of forex trading are easy to understand, such as how a currency might increase (but not always) in value when a central bank raises interest rates, other aspects can be more complex. You’ll need to learn the fundamentals of forex trading online before getting started in the markets. You’ll need to understand that there is someone else on the other end of your trade, and that can form difficult waters for beginners to navigate. Of course, there are forex trading tools for beginners, such as copy trading (your trades will automatically mimic that of a chosen expert trader), but becoming au fait with the world of forex is paramount. 
    2.	Start Trading on a Demo Account First 
    Online trading platforms will offer a wealth of tools for all levels of forex trading. Some, such as MetaTrader 4 (a specialised forex trading platform widely used online) may look complex and daunting, but beginners can quickly get the hang of it. That said, a good avenue to pursue is to launch of a demo forex trading account first. Give yourself at least a few weeks of forex trading with a demo account, and then start honing your strategy before entering the arena with real money. Most of the best online trading platforms offer risk-free demo accounts, giving you access to all the tools professionals use. It’s a good way to adjust your strategy (we would recommend not starting for real until you have simulated profits with a demo account), and it’s also a good way to learn if the online broker is the right fit for you. 
    3.	Build a Strategy for your Forex Trading 
    One aspect of trading that can trip up beginners is not knowing exactly what type of trader they are, nor what their goals are beyond securing a profit. For example, broadly speaking, there are three types of forex traders – short-term traders (scalpers and day traders), medium-term traders (hold positions for days), and long-term traders (willing to patiently hold for weeks and months). There are many variations within those three categories, but it is sufficient to demonstrate what we mean. Nonetheless, you’ll want to start building a strategy based on the type of trader you are. There’s nothing to say that you can’t combine different types of trades; day traders will often have long-term holds. The overall point is to create a strategy based on your goals, as well as the amount of time and dedication you wish to commit to forex trading. 
    
    4.	Employ Money Management and Risk Mitigation
    All good traders have a money plan. That’s not to be confused with a trading strategy. Rather, it refers to working out a blueprint for your investment and your goals. Traders should never invest more than they can afford to lose, for example, and it’s important to have a plan for taking profits. Risk management is just as important. Online trading platforms have a variety of tools that help you mitigate risks, including stop-loss functions. Once you get the experience, you’ll be more comfortable trading with leverage, but that, too, carries risks. The best rule of thumb for beginners is to have both profit and loss levels that they are comfortable with and willing to stick to. 

    5.	Keep Your Emotions in Check while Trading 
    The final rule might be the most important of all. Emotions get the best of traders in all types of markets, and those who keep a cool head tend to end up the most successful. The point, as such, is that emotional traders follow their hearts, not their heads. They are unable to cut losses or secure profits because they follow what they want to happen, not what market indicators point to what will happen. While this is likely the most important rule for trading forex, it’s also the hardest to follow. Even the world’s most famous traders – let’s take Michael Burry of “The Big Short” fame as an example – can be guilty of making mistakes due to wanting something to happen. Sometimes your intuition is right and the data is wrong, and vice versa. But keeping a cool head – and sometimes exiting the market altogether – will serve you best of all. 
    """
        else:
            original_article_content = test_article_content
        self.ask_gpt(original_article_content)
        self.parse_response()
        print(self.get_original_response())
        print(self.parse_response())
        pprint(self.parse_response())
        self.print_uncopyable_response()
        self.copy_parsed_response()
        self.print_copyable_response()
    
if __name__ == "__main__":
    gpt = GPTAsker(key_path="auth/openai_api_key.config") # , rewrite_article=True)
    gpt.test_all()
    
# check that the abstract and summary are correct