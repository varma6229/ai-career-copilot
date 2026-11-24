import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import extract_text_from_content

# Test 1: List with dictionary containing extras and signature (as returned by langchain-google-genai / Gemini)
raw_gemini_output = [{'type': 'text', 'text': 'Your name is Manivarma Lokani.', 'extras': {'signature': 'Eu8HCuwHAWkUfRNxh/uDubif+O9vV/gSpHoqI+K7QrM2OeImVQJiNNPQFBQsjOfMaiK+0DiGWPUNA6RBp+uWMbwfQphpjAx+Uru3uopldcSr22zxevltkF7reVh3+EaWbgebz2xzf7nFrHYMdvKKyw0TXFmU07WiK+OitSrO3ZACDxO+pYzq35OvhcaZRDaWe96H+NHLUFXUtnd1E9etP66rzffwnvsfLKHsv2H05KqyoH4GT7zeRWw9UP6G84Cr6TNgMxsnhuHOE/8FuzA1wk7UGdSA+l0Th77hymlCp4ls+C7FnjnTTqZskaU2go4vYMhuBIzgtOdQ4aEiZ/yeGGldo6xO8b5Fo0FqnozZ1npUwlwbd9ir9jWEbf1M840ohlOG85gz9YKn5e8QvYA1bFC3leMVYDOJ5XuvMiGIsPu7MqCVsAS3Hh3+DQzZ5Uxb0Vi75dTSlbrGMRLZp3aGYzuim/O/2jwuRofuP9MKPOfYZGGlqnf0ScRdnQMaIfR62CLvkDA9/tU8rDlpWfwrokv7QP5pxdEKnwV6x2Bul6Yo0Q+7LM04406TUk/SymHhoPFoBeZZ1SvSGRO3+AMP57scJA+v/aveX+o27y4sqDUjlmXCDNPqjakRvTBqH1e2LHtobftQyytbA1adsQOT82/MfH+Jyz7QXgJfGeahl8fDxcX9+aC2kX3hnlR3pG86yptXkDbzoJN7TRIs/EXO50kGURkIEk4YGkqauOzU2ru+FfpFygkXRXRitEPPcw+E9uARfa/j4J/zKalApXJOrHjRYkYwGggRg030TmNHoNuPYYSmDRXuH9J9SJWQVvuW1y/ebrH4jXD4o9ZCM13Yb2bpqvYcWdi0PjZ+nchTZrNHNlUqC4hA4RIVfdpBOZORoe2NaazdAUlZmeE10H45OnFPpEAQOHtv2ImZv4A7+1aLnauql4H/2VYawQjao+CanJxbY2PNVpmX1XqWnkNPVDcvZkIUH2ZgReIH674jlDNTd0ygyipWkbEux9eOZMq2wCRZcDt4gGdVycrfHdCjd5qBQQa8fcSTESS4jKMWTg1YWkSUkY/JPoUNGa2SMI6XuIno3WBvje5KC7u3sqzH+EcK2L0dmINhDgeXY7oFiY6RfD5Ed7TPVjZvDO66rc8qzeDNsv4856uniSdfJc6MMpJnPNZp76yH4M+dFig06sPXlcP3l980a9OHvTnX0yMH5I39FVredNigVIW1u5SEHY/ifuDKMrYV2dSWMUT/woTR3QhKDdJ2DkfUpFx6NPAZjEVD98psaY7OiB9hVA5CBqK5NPQN11n0ltbuylAeaLMQfwtJX714TiUbJ8DjpuT1knc='}}]
assert extract_text_from_content(raw_gemini_output) == 'Your name is Manivarma Lokani.'

# Test 2: Multiple chunks
multi_chunks = [
    {'type': 'text', 'text': 'Based on your resume, you are studying at '},
    {'type': 'text', 'text': '**Sreenidhi Institute of Science and Technology**.'}
]
assert extract_text_from_content(multi_chunks) == 'Based on your resume, you are studying at **Sreenidhi Institute of Science and Technology**.'

# Test 3: Stringified representation
assert extract_text_from_content(str(raw_gemini_output)) == 'Your name is Manivarma Lokani.'

# Test 4: Plain string
assert extract_text_from_content("Hello world") == "Hello world"

print("All extract_text_from_content tests passed successfully!")
