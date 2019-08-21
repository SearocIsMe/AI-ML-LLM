package com.ml.nyc;

import org.python.util.PythonInterpreter;

public class LuanchPython {
	public static void main(String[] args) {
		try {
			String strPythonFile = args[0];
			System.out.println("Java side, call python: " + strPythonFile);
			PythonInterpreter.initialize(System.getProperties(), System.getProperties(), new String[0]);
			PythonInterpreter interp = new PythonInterpreter();
			interp.execfile(strPythonFile);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}