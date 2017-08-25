package com.sort;

public class Sort {
	/**
	 * 冒泡排序 升序
	 * 
	 * 冒泡排序平均时间和最坏情况下（逆序）时间为o（n^2）
	 * 
	 * @param srcArray
	 */
	public static void bubbleSort(int[] srcArray) {
		// n-1次
		for (int i = 0; i < srcArray.length - 1; i++) {
			// n -1 -i 次 每比较一轮就会少一个需要对比
			for (int j = 0; j < srcArray.length - 1 - i; j++) {
				if (srcArray[j] > srcArray[j + 1]) {// 让大的数沉到最尾端，小的就“冒泡”了
					int temp = srcArray[j];
					srcArray[j] = srcArray[j + 1];
					srcArray[j + 1] = temp;
				}
			}
		}
	}

	/**
	 * 快速排序，最好的情况下时间复杂度o(n*log(n)) 最糟的情况下o(n^2) 有序的时候不适用快速排序，时间复杂度低
	 * 
	 * @param srcArray
	 * @param low
	 * @param high
	 */
	public static void quickSort(int[] srcArray, int low, int high) {
		int pivot = srcArray[low];// 基准值
		int i = low;
		int j = high;
		if (i >= j) {
			return;
		}
		while (i < j) {// 双向扫描
			while ((i < j) && srcArray[j] >= pivot) {// 向左扫描
				j--;
			}
			srcArray[i] = srcArray[j];
			while ((i < j) && srcArray[i] <= pivot) {// 向右扫描
				i++;
			}
			srcArray[j] = srcArray[i];
		}
		srcArray[i] = pivot;
		System.out.println(i + "==一次排序==" + j);
		quickSort(srcArray, low, i - 1);// 左边快速排序
		quickSort(srcArray, i + 1, high);// 右边快速排序
	}
}
