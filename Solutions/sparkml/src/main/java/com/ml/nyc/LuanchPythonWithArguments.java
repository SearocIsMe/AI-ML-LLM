package com.ml.nyc;

import org.python.util.PythonInterpreter;

public class LuanchPythonWithArguments {
	public static void main(String[] args) {
		try {
			String strPythonFile = args[0];
			String dataFile = args[1];
			System.out.println("Java side, call python: " + strPythonFile);
			System.out.println("args aize: " + args.length);
			System.out.println("Java side, data file: " + dataFile);

			PythonInterpreter.initialize(System.getProperties(), System.getProperties(), new String[0]);
			PythonInterpreter interp = new PythonInterpreter();
			interp.execfile(strPythonFile);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}