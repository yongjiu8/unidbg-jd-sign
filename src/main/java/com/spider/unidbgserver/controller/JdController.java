package com.spider.unidbgserver.controller;

import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONException;
import com.spider.unidbgserver.service.JdService;
import com.spider.unidbgserver.utils.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/jd")
public class JdController{

    @Autowired
    JdService jdService;

    @RequestMapping("/sign")
    public R getSign(String functionId, String body){
        if (StrUtil.isEmpty(functionId) || StrUtil.isEmpty(body)){
            return R.fail(-1, "参数异常！");
        }
        try {
            JSONObject jsonObject = JSONUtil.parseObj(body);
        }catch (Exception e){
            System.out.println(e);
            return R.fail(-1, "body参数异常！");
        }
        String uuid = StrUtil.uuid();
        String sign = jdService.getSign(functionId, uuid, body);
        String res = "&clientVersion=11.0.2&build=97565&client=android&partner=yyds3&sdkVersion=30&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=" + uuid + "&uuid=" + uuid + "&" + sign;
        return R.success("成功！", res);
    }

}
