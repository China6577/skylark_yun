import json
# 认证模块
from tencentcloud.common import credential
# 客户端类
from tencentcloud.common.profile.client_profile import ClientProfile
# Http配置类
from tencentcloud.common.profile.http_profile import HttpProfile
# 异常类
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 创建短信客户端和包含短信所需的请求模型
from tencentcloud.sms.v20210111 import sms_client, models
from django.conf import settings

class TencentSMS:
    """
    腾讯云短信服务封装类，用于发送短信。
    """

    def __init__(self):
        """
        初始化腾讯云短信客户端。
        使用 Django 配置中的 SecretId 和 SecretKey 进行认证。
        """
        # 使用 Django 配置中的 SecretId 和 SecretKey 创建认证对象
        self.cred = credential.Credential(settings.TENCENT_SMS['SecretId'], settings.TENCENT_SMS['SecretKey'])

        # 配置 HTTP 请求选项
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 设置 API 请求的端点

        # 配置客户端选项
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        # 创建短信客户端对象
        self.client = sms_client.SmsClient(self.cred, settings.TENCENT_SMS['REGION'], clientProfile)

    def send_sms(self, phone_number, template_param_set):
        """
        发送短信。

        :param phone_number: 接收短信的手机号码。
        :param template_param_set: 短信模板参数列表。
        :return: 返回短信发送结果的 JSON 字符串，如果发生异常则返回错误信息。
        """
        try:
            # 创建短信发送请求对象
            req = models.SendSmsRequest()

            # 设置请求参数
            params = {
                "PhoneNumberSet": [phone_number],  # 接收短信的手机号码列表
                "SmsSdkAppId": settings.TENCENT_SMS['SMS_SDK_APP_ID'],  # 短信应用 ID
                "TemplateId": settings.TENCENT_SMS['TEMPLATE_ID'],  # 短信模板 ID
                "SignName": settings.TENCENT_SMS['SIGN_NAME'],  # 短信签名
                "TemplateParamSet": [template_param_set]  # 短信模板参数列表
            }

            # 将参数转换为 JSON 字符串并设置到请求对象中
            req.from_json_string(json.dumps(params))

            # 发送短信并获取响应
            resp = self.client.SendSms(req)

            # 返回响应结果的 JSON 字符串
            return resp.to_json_string()
        except TencentCloudSDKException as err:
            # 捕获并返回腾讯云 SDK 异常信息
            return str(err)