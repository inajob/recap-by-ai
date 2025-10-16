python get-same-month.py --deep > out/out-deep.txt
python get-same-month.py > out/out-shallow.txt

# python chat.py prompts/prelude-health.txt out/out-shallow.txt > out/health-advice.txt
# python chat.py prompts/prelude-childcare.txt out/out-deep.txt > out/childcare-advice.txt
# python chat.py prompts/prelude-hobby.txt out/out-deep.txt > out/hobby-advice.txt
python chat.py prompts/prelude-work.txt out/out-deep.txt > out/work-advice.txt
