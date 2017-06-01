#!/usr/bin/python
import sys
import re

default_ban_list = "stereo|mono|remaster|edit|bonus|extended|demo|explicit|version|feat"
compiled_ban_list = ""
inside_brackets = None
after_delimiter = None

def compile_re(expr, ban_list = default_ban_list):
	expr = expr.replace("BAN_LIST_HERE", ban_list)
	return re.compile(expr, re.IGNORECASE)

def compile_all(ban_list = default_ban_list):
	global inside_brackets 
	global after_delimiter
	inside_brackets = compile_re(r"([\(\[][^)\]]*?(BAN_LIST_HERE)[^)\]]*?[\)\]])",ban_list)
	after_delimiter = compile_re(r"([\-,;/])([^\-,;/])*(BAN_LIST_HERE).*", ban_list)
	compiled_ban_list = ban_list

def fix_title(title, ban_list = default_ban_list):
	if ban_list != compiled_ban_list:
		compile_all(ban_list)
	title = re.sub(inside_brackets, "", title)
	title = re.sub(after_delimiter, "", title)
	return title.strip()
	
def test():
	assert fix_title("Ziggy Stardust (Remastered)", "stereo") == "Ziggy Stardust (Remastered)"
	assert fix_title("Ziggy Stardust [Stereo]") == "Ziggy Stardust"
	assert fix_title("Ziggy Stardust [Stereo] [Live]", "mono|live") == "Ziggy Stardust [Stereo]"
	assert fix_title("Ziggy Stardust [Remastered]") == "Ziggy Stardust"
	assert fix_title("Ziggy Stardust (Remastered 2017)") == "Ziggy Stardust"
	assert fix_title("Ziggy Stardust - Remastered 2017") == "Ziggy Stardust"
	assert fix_title("Ziggy Stardust - Remastered 2017 Version") == "Ziggy Stardust"
	assert fix_title("Cat People (Putting Out Fire) - 1999 Remastered Version") == "Cat People (Putting Out Fire)"
	assert fix_title("Cat People (Putting Out Fire) (1999 Remastered Version)") == "Cat People (Putting Out Fire)"
	assert fix_title("Space Oddity - Live") == "Space Oddity - Live"
	assert fix_title("Space Oddity - Live", "live") == "Space Oddity"
	assert fix_title("Layla - 40th Anniversary Version / 2010 Remastered") == "Layla"
	assert fix_title("AAA (Bonus)") == "AAA"
	assert fix_title("Alabama Song - Whisky Bar - Remastered 2008") == "Alabama Song - Whisky Bar"
	assert fix_title("Doctor Alibi - feat. Lemmy Kilmister") == "Doctor Alibi"

	print "Tests passed!"

def usage():
	file = sys.argv[0]
	print """standard usage: FILENAME <title> [--ban-list \"word1|word2|word3\"]
to run tests: FILENAME --test""".replace("FILENAME", file)
	sys.exit(1)

def main():
	args = sys.argv
	argc = len(sys.argv)
	ban_list = default_ban_list

	if argc <= 1:
		usage()
	if "--test" in args:
		test()
		sys.exit(0)

	if "--ban-list" in args:
		pos = args.index("--ban-list")
		if argc <= pos + 1:
			usage()
		else:
			ban_list = args[pos+1]
			args[pos:pos+2] = []
			argc -= 2

	for i in xrange(1, argc):
		print fix_title(args[i], ban_list)
	

if __name__ == "__main__":
	main()
