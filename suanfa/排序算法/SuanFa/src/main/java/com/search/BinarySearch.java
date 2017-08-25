package com.search;

/**
 * 
 * @author 王辉阳
 * @date 2017年7月23日 下午9:44:11
 * @Description 二分查找
 * 
 *              数据库的B-Tree索引就是基于二分查找的原理
 */
public class BinarySearch {
	/**
	 * 二分查找 递归实现
	 * 
	 * @param srcArray
	 *            升序的数组
	 * @param destNum
	 *            所要查询的数
	 * @param low
	 *            起始下标
	 * @param high
	 *            结束下标
	 * @return 目标下标
	 */
	public static int biSearchRecurse(int[] srcArray, int destNum, int low, int high) {
		int middle = (low + high) / 2;
		if (destNum == srcArray[middle]) {
			return middle;
		}
		if ((destNum > srcArray[middle]) && (low <= high)) {// 去右侧找
			return biSearchRecurse(srcArray, destNum, middle + 1, high);
		}
		if ((destNum < srcArray[middle]) && (low <= high)) {// 去左侧找
			return biSearchRecurse(srcArray, destNum, low, middle - 1);
		}
		return -1;
	}

	/**
	 * 二分查找 非递归实现
	 * 
	 * @param srcArray
	 *            升序的数组
	 * @param destNum
	 *            所要查询的数
	 * @return 目标下标
	 */
	public static int biSearch(int[] srcArray, int destNum) {
		int low = 0;
		int high = srcArray.length - 1;
		int middle = (low + high) / 2;
		if (destNum == srcArray[middle]) {
			return middle;
		}
		while (low < high) {
			if ((destNum > srcArray[middle])) {
				low = middle + 1;
			}
			if ((destNum < srcArray[middle])) {
				high = middle - 1;
			}
			middle = (low + high) / 2;
			if (destNum == srcArray[middle]) {
				return middle;
			}
		}
		return -1;
	}
}
