package com.search;

import org.junit.Test;

import com.sort.Sort;

public class BinarySearchTest {
	@Test
	public void biSearchRecurse() {
		int[] srcArray = new int[] { 12, 4, 10, 44, 20, 6, 5, 10 };
		Sort.quickSort(srcArray, 0, srcArray.length - 1);
		// 返回找到的下标：6
		int index = BinarySearch.biSearchRecurse(srcArray, 20, 0, srcArray.length - 1);
		System.out.println(index);
		// -1表示不存在
		index = BinarySearch.biSearchRecurse(srcArray, 210, 0, srcArray.length - 1);
		System.out.println(index);
	}

	@Test
	public void biSearch() {
		int[] srcArray = new int[] { 12, 4, 10, 44, 20, 6, 5, 10 };
		Sort.quickSort(srcArray, 0, srcArray.length - 1);
		// 返回找到的下标：6
		int index = BinarySearch.biSearchRecurse(srcArray, 20, 0, srcArray.length - 1);
		System.out.println(index);
		// -1表示不存在
		index = BinarySearch.biSearchRecurse(srcArray, 210, 0, srcArray.length - 1);
		System.out.println(index);
	}
}
