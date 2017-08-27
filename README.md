# Hitcon-CMT-2017-Wargame

從src可以看到跟server的所有通訊都被加密過，用的是AES-CBC加密。

* 由於固定IV，server的明文固定時，密文也固定
* 而我們的IV可控，只要看看[CBC mode](https://zh.wikipedia.org/wiki/%E5%88%86%E7%BB%84%E5%AF%86%E7%A0%81%E5%B7%A5%E4%BD%9C%E6%A8%A1%E5%BC%8F#.E5.AF.86.E7.A0.81.E5.9D.97.E9.93.BE.E6.8E.A5.EF.BC.88CBC.EF.BC.89)的解密部份就可以發現藉由已經得到的明文密文pair(可以用「Welcome!!」或是「command not found」)去構造IV使得解出來的第一個block明文變得可控，因此可以將其控成「get-flag」開頭得到加密過後的flag內容
* 已知flag的開頭為「hitcon{」，因此可以猜測第一個字元，並且用前面控制IV的方法嘗試將明文控成「get-flag」開頭，如果猜對的話就會得回跟原本一樣的加密過後的flag，因此最多需要嘗試所有可見字元即可找出第一個字元
* 由於msg有被strip過，開頭和結尾的空白字元都會在strip的時候被移除掉，因此將明文控成「 get-flag」開頭也是可以的，因此可以用同樣的方法猜剩下的字元
* 但是我們其實可控的明文只有第一個block，而flag的長度顯然不只，而server提供了echo command，可以用echo來把flag前面移除掉，並重複前面的步驟即可得到flag
