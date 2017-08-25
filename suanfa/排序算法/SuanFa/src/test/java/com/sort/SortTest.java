package com.sort;

import org.junit.Test;

public class SortTest {
	@Test
	public void bubbleSort() {
		int[] srcArray = new int[] { 12, 4, 10, 44, 20, 6, 5, 10 };
		Sort.bubbleSort(srcArray);
		printArray(srcArray);
	}

	@Test
	public void quickSort() {
		int[] srcArray = new int[] { 12, 4, 10, 44, 20, 6, 5, 10 };
		Sort.quickSort(srcArray, 0, srcArray.length - 1);
		printArray(srcArray);
	}

	private void printArray(int[] srcArray) {
		for (int i = 0; i < srcArray.length; i++) {
			if (i != srcArray.length - 1) {
				System.out.print(srcArray[i] + ",");
			} else {
				System.out.print(srcArray[i]);
			}
		}
	}
}
