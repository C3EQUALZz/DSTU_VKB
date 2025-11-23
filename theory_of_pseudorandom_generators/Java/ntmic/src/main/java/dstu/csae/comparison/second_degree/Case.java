package dstu.csae.comparison.second_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.mathutils.MathUtils;

public interface Case {

   static boolean matches(Comparison comparison) {
      if (!MathUtils.isPrime(comparison.getField())) {
         return false;
      }
      if (Symbol.getLegendreSymbol(comparison) < 0) {
         return false;
      }
      if (comparison.getField() == 2){
         return false;
      }
      if (comparison.getRemains() % comparison.getField() == 0){
         return false;
      }
      return true;
   }

   static int getSolutionCount(Comparison squareComparison){
      if(!matches(squareComparison)){
         return 0;
      }
      if(Symbol.getLegendreSymbol(squareComparison) == 0){
         return 1;
      }
      return  2;
   }

}
