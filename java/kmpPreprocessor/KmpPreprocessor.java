public class KmpPreprocessor {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");

        if (args.length == 1) {
        	// blah
        	String pattern = args[0];
        	int lps[] = getLps(pattern);

        	printLps(pattern, lps);
        } else {
        	System.out.printf("Error: Exactly one argument expected.  Received %d\n", args.length);
        }
    }

    public static int[] getLps(String pattern) {
    	int lps[] = new int[pattern.length()];

    	// TODO: Check for empty string
    	// no look-back for first character
    	lps[0] = 0;

    	int substringLength = 0;
    	int i = 1; // start at second entry

    	while (i < pattern.length()) {
    		// if the current character matches the next character in the current substring prefix
    		if (pattern.charAt(i) == pattern.charAt(substringLength)) {
    			substringLength += 1;
    			lps[i] = substringLength;
    			i += 1;
    		} else {
    			// try again with a smaller "inner" substring
    			//  (i.e. if current substring prefix itself contains a substring up to the last character in it)
    			if (substringLength > 0) {
    				substringLength = lps[substringLength-1];
    			}
    			// else, no smaller possible substring right now; restart with no match at this position
    			else {
    				lps[i] = 0;
    				i++;
    			}
    		}
    	}

    	return lps;
    }

    /* Utility functions (display only) */

    public static void printLps(String pattern, int[] lps) {
    	// TODO: Assert pattern and lps are the same length
    	// TODO: This output will display poorly when LPS entries are multiple digits
    	String patternSplit[] = pattern.split("");
    	String patternSpaced = String.join(" ", patternSplit);

    	String lpsSplit[] = intArrayToStringArray(lps);
    	String lpsSpaced = String.join(" ", lpsSplit);

    	System.out.printf("Pattern: %s\n", patternSpaced);
    	System.out.printf("LPS:     %s\n", lpsSpaced);
    }

    public static String[] intArrayToStringArray(int[] intArray) {
    	String stringArray[] = new String[intArray.length];
    	for (int i=0; i < intArray.length; i++) {
    		stringArray[i] = Integer.toString(intArray[i]);
    	}
    	return stringArray;
    }

}
