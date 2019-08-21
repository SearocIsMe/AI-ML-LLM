package com.ml.nyc;

import org.python.util.PythonInterpreter;

public class LuanchPythonWithArguments {
	public static void main(String[] args) {
		try {
			String strPythonFile = args[0];
			System.out.println("Java side, call python: " + strPythonFile);
			System.out.println("args[0]: " + strPythonFile);
			System.out.println("args[1]: " + args[1].toString());
			System.out.println("args[2]: " + args[2].toString());

			String arrParas[] = { args[1], args[2] };
			PythonInterpreter.initialize(System.getProperties(), System.getProperties(), arrParas);
			PythonInterpreter interp = new PythonInterpreter();
			interp.execfile(strPythonFile);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}