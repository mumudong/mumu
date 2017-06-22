/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.asiainfo.dacp.platform.hive.udf.generic;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.hive.ql.udf.UDFType;
import org.apache.hadoop.io.Text;

/**
 * UDFIDTrans
 */

@UDFType(deterministic = false)
@Description(name = "transid", value = "_FUNC_(idNo[15][18]) -  returns 18 ID card number, if the character contains x, then x is converted to 10", extended = "Example:\n"
		+ "> SELECT transid('51021491810624173x') FROM src LIMIT 1;" + "510214918106241710\n")

public class UDFIDTrans extends UDF {

	public UDFIDTrans() {

	}
	Text result = new Text();
	public Text evaluate(Text dateText) {
		if (dateText == null) {
			result.set("parameter is null");			
		}
		try {
			String res = getEighteenIDCard(dateText.toString());
			result.set(res);

		} catch (Exception e) {
			result.set(dateText.toString() + "error");

		}
		return result;
	}

	/**
	 * 判断身份证号码中是否包含字母X或者x,如果有X/x则把X/x替换成10;否则原样返回
	 * 
	 * @param 身份证号码
	 * @return 转换后的身份证号码
	 */
	public String haveX(String IDCard) {
		String ID = IDCard;
		String re = "^\\d+[\\d|x|X]$";
		Matcher m = Pattern.compile(re).matcher(IDCard);
		if (m.matches()) {
			String newID = ID.replaceAll("[Xx]", "10");
			return newID;
		} else {
			return IDCard;
		}

	}

	/**
	 * 15位身份证号码补全为18位
	 * 
	 * @param 15/18位身份证号码
	 * @return 18位身份证号码
	 * @throws Exception
	 */
	public String getEighteenIDCard(String IDCard) {
		Matcher eighteenM = Pattern.compile("^\\d+[\\d|x|X]$").matcher(IDCard);
		Matcher fifTeenM = Pattern.compile("^\\d+$").matcher(IDCard);
		if (IDCard != null && IDCard.length() == 15 && fifTeenM.matches()) {
			StringBuilder sb = new StringBuilder();
			sb.append(IDCard.substring(0, 6)).append("19").append(IDCard.substring(6));
			sb.append(getVerifyCode(sb.toString()));
			return sb.toString();
		} else if (IDCard != null && IDCard.length() == 18 && eighteenM.matches()) {
			return IDCard;
		} else {
			return IDCard + " is error";
		}
	}

	/**
	 * 获取15位升级到18位的校验码
	 * 
	 * @param idCardNumber
	 * @return verifyCode
	 * @throws Exception
	 */
	public char getVerifyCode(String idCardNumber) {
		char[] Ai = idCardNumber.toCharArray();
		int[] Wi = { 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 };
		char[] verifyCode = { '1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2' };
		int S = 0;
		int Y;
		for (int i = 0; i < Wi.length; i++) {
			S += (Ai[i] - '0') * Wi[i];
		}
		Y = S % 11;
		return verifyCode[Y];
	}
}
